package org.fao.geonet.listener;

import java.text.Normalizer;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.fao.geonet.domain.Language;
import org.fao.geonet.domain.Source;
import org.fao.geonet.domain.SourceType;
import org.fao.geonet.repository.LanguageRepository;
import org.fao.geonet.repository.SourceRepository;
import org.springframework.stereotype.Component;

@Component
public class VirtualCatalogService {
    SourceRepository sourceRepository;
    LanguageRepository langRepository;

    public VirtualCatalogService(SourceRepository sourceRepository, LanguageRepository langRepository) {
        this.sourceRepository = sourceRepository;
        this.langRepository = langRepository;
    }

    public void configurePortal(String uuid, String title, List<String> uuids) {
       Source source = sourceRepository.findById(uuid)
            .orElseGet(() -> {
                Source newSource = new Source();
                newSource.setUuid(uuid);
                newSource.setType(SourceType.subportal);
                return newSource;
            });

        source.setName(sanitizeAndTrimTitle(title));
        source.setFilter(String.format("+uuid:(%s)", uuids.stream()
            .map(e -> "\"" + e + "\"")
            .collect(Collectors.joining(" or "))));

        java.util.List<Language> allLanguages = langRepository.findAll();
        Map<String, String> labelTranslations = source.getLabelTranslations();
        // TODO: Get translations from the record (or let config from the admin, override the title)?
        for (Language l : allLanguages) {
            String label = title; // labelTranslations.get(l.getId());
            source.getLabelTranslations().put(l.getId(),
                label == null ? source.getName() : label);
        }

        // TODO: logo?
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
}
