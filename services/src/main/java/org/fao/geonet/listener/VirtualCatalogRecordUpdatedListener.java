package org.fao.geonet.listener;

import org.fao.geonet.constants.Geonet;
import org.fao.geonet.domain.AbstractMetadata;
import org.fao.geonet.events.history.RecordUpdatedEvent;
import org.fao.geonet.kernel.datamanager.base.BaseMetadataUtils;
import org.fao.geonet.utils.Log;
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

    public VirtualCatalogRecordUpdatedListener(BaseMetadataUtils metadataUtils, VirtualCatalogService virtualCatalogService) {
        this.metadataUtils = metadataUtils;
        this.virtualCatalogService = virtualCatalogService;
    }

    @Override
    public void onApplicationEvent(RecordUpdatedEvent event) {
        AbstractMetadata metadata = metadataUtils.findOne(String.valueOf(event.getMdId()));
        if (!metadata.getDataInfo().getSchemaId().equals("dcat-ap")) {
            return;
        }
        try {
            if (metadataUtils.isMetadataDraft(event.getMdId().intValue())) {
                return;
            }
        } catch (Exception e) {
            Log.error(Geonet.GEONETWORK, String.format("Could not check whether record is draft or not. Related info: mdId(%s)", event.getMdId()));
            return;
        }

        virtualCatalogService.catalogUpdated(metadata);
    }
}
