package org.fao.geonet.listener;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.fao.geonet.constants.Geonet;
import org.fao.geonet.domain.AbstractMetadata;
import org.fao.geonet.events.history.RecordUpdatedEvent;
import org.fao.geonet.kernel.SchemaManager;
import org.fao.geonet.kernel.datamanager.base.BaseMetadataUtils;
import org.fao.geonet.kernel.schema.SchemaPlugin;
import org.fao.geonet.utils.Log;
import org.fao.geonet.utils.Xml;
import org.jdom.Element;
import org.jdom.Namespace;
import org.jdom.Text;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Component;

/**
 * Listener for metadata updates that checks if the updated record is a virtual catalog
 * and updates the associated portal configuration accordingly.
 */
@Component
public class VirtualCatalogRecordUpdatedListener implements ApplicationListener<RecordUpdatedEvent> {
    private final BaseMetadataUtils metadataUtils;
    private final VirtualCatalogService virtualCatalogService;
    private final SchemaManager schemaManager;

    public VirtualCatalogRecordUpdatedListener(BaseMetadataUtils metadataUtils, VirtualCatalogService virtualCatalogService, SchemaManager schemaManager) {
        this.metadataUtils = metadataUtils;
        this.virtualCatalogService = virtualCatalogService;
        this.schemaManager = schemaManager;
    }

    @Override
    public void onApplicationEvent(RecordUpdatedEvent event) {
        AbstractMetadata metadata = metadataUtils.findOne(String.valueOf(event.getMdId()));
        if (!metadata.getDataInfo().getSchemaId().equals("dcat-ap")) {
            return;
        }

        try {
            Element xml = metadata.getXmlData(false);
            SchemaPlugin schemaPlugin = schemaManager.getSchemaPlugin(metadata.getDataInfo().getSchemaId());

            List<Namespace> namespaces = new ArrayList<>(schemaPlugin.getNamespaces());
            // Check if virtual catalog
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

            virtualCatalogService.configurePortal(metadata.getUuid(), catalogTitle, uuids);
        } catch (Exception ex) {
            Log.error(Geonet.DATA_MANAGER, "Metadata update: Virtual catalog update error " + event.getSource(), ex);
        }
    }
}
