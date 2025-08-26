package org.fao.geonet.listener;

import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.apache.logging.log4j.util.Strings;
import org.fao.geonet.constants.Geonet;
import org.fao.geonet.domain.AbstractMetadata;
import org.fao.geonet.domain.Language;
import org.fao.geonet.domain.Source;
import org.fao.geonet.domain.SourceType;
import org.fao.geonet.kernel.SchemaManager;
import org.fao.geonet.kernel.schema.SchemaPlugin;
import org.fao.geonet.repository.LanguageRepository;
import org.fao.geonet.repository.SourceRepository;
import org.fao.geonet.utils.Log;
import org.fao.geonet.utils.Xml;
import org.jdom.Element;
import org.jdom.Namespace;
import org.jdom.Text;
import org.springframework.stereotype.Component;

@Component
public class VirtualCatalogService {
    SourceRepository sourceRepository;
    LanguageRepository langRepository;
    SchemaManager schemaManager;

    public VirtualCatalogService(SourceRepository sourceRepository, LanguageRepository langRepository, SchemaManager schemaManager) {
        this.sourceRepository = sourceRepository;
        this.langRepository = langRepository;
        this.schemaManager = schemaManager;
    }

    public void catalogUpdated(AbstractMetadata metadata) {
        try {
            Element xml = metadata.getXmlData(false);
            SchemaPlugin schemaPlugin = schemaManager.getSchemaPlugin(metadata.getDataInfo().getSchemaId());
            List<Namespace> namespaces = new ArrayList<>(schemaPlugin.getNamespaces());

            // Check if the record is a virtual catalog
            if (!Xml.selectBoolean(xml, "dcat:Catalog[not(//dcat:Dataset) and not(//dcat:DataService)]/dct:title", namespaces)) {
                return;
            }

            // Extract catalog title
            String catalogTitle = "";
            Object o = Xml.selectSingle(xml, "dcat:Catalog/dct:title/text()", namespaces);
            if (o instanceof Text) {
                catalogTitle = ((Text)  o).getTextTrim();
            }

            // Extract associated record UUIDs
            List<String> uuids = Xml.selectNodes(xml, "dcat:CatalogRecord/dct:identifier/text()", namespaces)
                .stream()
                .map(e -> ((Text) e).getTextTrim())
                .filter(uuid -> !uuid.equals(metadata.getUuid()))
                .collect(Collectors.toList());
            uuids.add(metadata.getUuid());

            // Configure the portal based on the above
            configurePortal(metadata.getUuid(), catalogTitle, uuids);
        } catch (Exception ex) {
            Log.error(Geonet.DATA_MANAGER, "Metadata update: Virtual catalog update error.", ex);
        }
    }

    public void configurePortal(String uuid, String title, List<String> uuids) {
        Source source = sourceRepository.findById(uuid)
            .orElseGet(() -> {
                Source newSource = new Source();
                newSource.setUuid(uuid);
                newSource.setServiceRecord(uuid);
                newSource.setType(SourceType.subportal);
                newSource.setListableInHeaderSelector(false);
                return newSource;
            });

        // if there is no name yet, use the record title as the starting value
        if (Strings.isBlank(source.getName())) {
            source.setName(sanitizeAndTrimTitle(title));
        }
        source.setFilter(String.format("+uuid:(%s)", uuids.stream()
            .map(e -> "\"" + e + "\"")
            .collect(Collectors.joining(" or "))));

        java.util.List<Language> allLanguages = langRepository.findAll();
        Map<String, String> lt = source.getLabelTranslations();
        for (Language l : allLanguages) {
            // only set the label translation if it is not present yet
            if(Strings.isBlank(lt.get(l.getId())))
            {
                lt.put(l.getId(),
                    title == null ? source.getName() : title);
            }
        }

        sourceRepository.save(source);
    }


    private String sanitizeAndTrimTitle(String title) {
        // Replace accented characters with non-accented characters
        String normalizedTitle = Normalizer.normalize(title, Normalizer.Form.NFD);
        String titleWithoutAccents = normalizedTitle.replaceAll("\\p{InCombiningDiacriticalMarks}+", "");

        // Replace non-regular characters with underscore
        return titleWithoutAccents
            .replaceAll("[^a-zA-Z0-9\\-]", "_")
            .replaceAll("_+", "_")
            .replace("..", "_")
            .trim();
    }

    public void removePortal(String uuid) {
        sourceRepository.findById(uuid).ifPresent(source -> sourceRepository.delete(source));
    }
}
