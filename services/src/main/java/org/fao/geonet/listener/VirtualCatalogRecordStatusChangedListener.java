package org.fao.geonet.listener;

import org.fao.geonet.constants.Geonet;
import org.fao.geonet.domain.MetadataDraft;
import org.fao.geonet.domain.StatusValue;
import org.fao.geonet.events.md.MetadataStatusChanged;
import org.fao.geonet.utils.Log;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Component;

/**
 * Listener for metadata updates that checks if the updated record is a virtual catalog
 * and updates the associated portal configuration accordingly.
 */
@Component
public class VirtualCatalogRecordStatusChangedListener implements ApplicationListener<MetadataStatusChanged> {
    private final VirtualCatalogService virtualCatalogService;

    public VirtualCatalogRecordStatusChangedListener(VirtualCatalogService virtualCatalogService) {
        this.virtualCatalogService = virtualCatalogService;
    }

    @Override
    public void onApplicationEvent(MetadataStatusChanged event) {
        try {
            // only update base records that were approved - this happens when creating a catalog from scratch
            boolean noDraft = !(event.getSource() instanceof MetadataDraft);
            boolean isApproved = event.getStatus().getId() == Integer.parseInt(StatusValue.Status.APPROVED);
            if(noDraft && isApproved) {
                virtualCatalogService.catalogUpdated(event.getMd());
            }
        } catch (Exception ex) {
            Log.error(Geonet.DATA_MANAGER, "Metadata update: Virtual catalog status change error " + event.getSource(), ex);
        }
    }
}
