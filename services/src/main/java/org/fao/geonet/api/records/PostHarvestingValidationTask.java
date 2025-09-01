//=============================================================================
//===	Copyright (C) 2001-2007 Food and Agriculture Organization of the
//===	United Nations (FAO-UN), United Nations World Food Programme (WFP)
//===	and United Nations Environment Programme (UNEP)
//===
//===	This program is free software; you can redistribute it and/or modify
//===	it under the terms of the GNU General Public License as published by
//===	the Free Software Foundation; either version 2 of the License, or (at
//===	your option) any later version.
//===
//===	This program is distributed in the hope that it will be useful, but
//===	WITHOUT ANY WARRANTY; without even the implied warranty of
//===	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
//===	General Public License for more details.
//===
//===	You should have received a copy of the GNU General Public License
//===	along with this program; if not, write to the Free Software
//===	Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
//===
//===	Contact: Jeroen Ticheler - FAO - Viale delle Terme di Caracalla 2,
//===	Rome - Italy. email: geonetwork@osgeo.org
//==============================================================================

package org.fao.geonet.api.records;

import org.apache.commons.lang.StringUtils;
import org.fao.geonet.ApplicationContextHolder;
import org.fao.geonet.constants.Geonet;
import org.fao.geonet.domain.HarvestHistory;
import org.fao.geonet.domain.Metadata;
import org.fao.geonet.kernel.datamanager.IMetadataValidator;
import org.fao.geonet.kernel.harvest.event.HarvesterTaskCompletedEvent;
import org.fao.geonet.repository.HarvestHistoryRepository;
import org.fao.geonet.repository.MetadataDraftRepository;
import org.fao.geonet.repository.MetadataValidationRepository;
import org.jdom.Element;
import org.jdom.JDOMException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.logging.LogLevel;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.event.TransactionPhase;
import org.springframework.transaction.event.TransactionalEventListener;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class PostHarvestingValidationTask extends ValidationTask {

    private boolean applyInternalValidation = true;
    private boolean applyRemoteInspireValidation = true;

    @Autowired
    MetadataDraftRepository metadataDraftRepository;

    @Autowired
    IMetadataValidator metadataValidator;

    @Autowired
    MetadataValidationRepository validationRepository;

    @Autowired
    HarvestHistoryRepository historyRepository;

    public PostHarvestingValidationTask() {
    }

    @EventListener
    @Async
    @TransactionalEventListener(
        phase = TransactionPhase.AFTER_COMMIT,
        fallbackExecution = true)
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void apply(HarvesterTaskCompletedEvent harvesterTaskCompletedEvent) {
        List<Metadata> harvesterRecords = metadataRepository.findAllByHarvestInfo_Uuid(
            harvesterTaskCompletedEvent.getHarvesterId()
        );

        // optimise the records that are validated, make sure we don't validate anything that doesn't need to be
        Optional<HarvestHistory> harvestHistory = historyRepository.findById(harvesterTaskCompletedEvent.getHarvestHistoryId());
        if (harvestHistory.isPresent()) {
            try {
                // retrieve the uuids that were created or modified by the harvester job
                Element infoAsXml = harvestHistory.get().getInfoAsXml();
                // createdUuids/modifiedUuids is not set by all harvesters - only optimise validation tasks if they are set
                if (infoAsXml != null &&
                    infoAsXml.getChild("createdUuids") != null &&
                    infoAsXml.getChild("modifiedUuids") != null) {
                    Set<String> uuidsToConsider = new HashSet<>();
                    Arrays.asList("createdUuids", "modifiedUuids").forEach(name -> {
                        Element uuids = infoAsXml.getChild(name);
                        if (uuids != null) {
                            Stream<Element> children = uuids.getChildren().stream()
                                .filter(e -> e instanceof Element);
                            children
                                .map(Element::getText)
                                .forEach(uuidsToConsider::add);
                        }
                    });
                    // remove uuids that were not created or modified, these don't have to be validated again
                    harvesterRecords.removeIf(m -> !uuidsToConsider.contains(m.getUuid()));
                }
            } catch (IOException | JDOMException e) {
                log(LogLevel.ERROR, "Could not parse harvest history to optimise validation task (harvester id {})", harvestHistory.get().getId());
            }
        }

        List<Integer> recordIds = harvesterRecords.stream().map(Metadata::getId).collect(Collectors.toList());
        log(LogLevel.DEBUG, "ValidationTask started on {} record(s)",
            recordIds.size());

        harvesterRecords.forEach(metadata -> {
            Instant start = Instant.now();

            log(LogLevel.DEBUG, "{} / Validation start.",
                metadata.getUuid());

            String schema = metadata.getDataInfo().getSchemaId();
            if (applyInternalValidation) {
                try {
                    metadataValidator.doValidate(metadata, Geonet.DEFAULT_LANGUAGE);
                } catch (Exception e) {
                    log(LogLevel.DEBUG, "{} / Internal Validation error. %s",
                        metadata.getUuid(), e.getMessage());
                }
            }

            if (applyRemoteInspireValidation) {
                if (schema.equals("iso19139")) { // TODO: Support ISO19115-3
                    ApplicationContextHolder.get().publishEvent(
                        new InspireValidationTask.Event(
                            ApplicationContextHolder.get(),
                            metadata.getId(),
                            false));
                } else {
                    log(LogLevel.DEBUG, "{} ({}) / Validation done in {}ms.",
                        metadata.getUuid(),
                        schema,
                        Duration.between(start, Instant.now()).toMillis());
                }
            }

            if (StringUtils.isNotEmpty(xsltPostProcess)) {
                applyXsltProcess(metadata);
            }

            try {
                metadataIndexer.indexMetadata(new ArrayList<>(
                    List.of(String.valueOf(metadata.getId()))));
            } catch (Exception e) {
                log(LogLevel.DEBUG, "{} / Error while indexing record: {}",
                    metadata.getUuid(), e.getMessage());
            }
        });
    }


    public boolean isApplyInternalValidation() {
        return applyInternalValidation;
    }

    public void setApplyInternalValidation(boolean applyInternalValidation) {
        this.applyInternalValidation = applyInternalValidation;
    }

    public boolean isApplyRemoteInspireValidation() {
        return applyRemoteInspireValidation;
    }

    public void setApplyRemoteInspireValidation(boolean applyRemoteInspireValidation) {
        this.applyRemoteInspireValidation = applyRemoteInspireValidation;
    }

    public String getXsltPostProcess() {
        return xsltPostProcess;
    }

    public void setXsltPostProcess(String xsltPostProcess) {
        this.xsltPostProcess = xsltPostProcess;
    }
}
