package org.fao.geonet.listener;

import java.util.ArrayList;
import java.util.List;
import org.fao.geonet.constants.Geonet;
import org.fao.geonet.events.history.RecordDeletedEvent;
import org.fao.geonet.kernel.SchemaManager;
import org.fao.geonet.kernel.datamanager.base.BaseMetadataUtils;
import org.fao.geonet.kernel.schema.SchemaPlugin;
import org.fao.geonet.utils.Log;
import org.fao.geonet.utils.Xml;
import org.jdom.Element;
import org.jdom.Namespace;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Component;

/**
 * Listener for metadata deleted that remove the corresponding portal configuration if any.
 */
@Component
public class VirtualCatalogRecordDeletedListener implements ApplicationListener<RecordDeletedEvent> {
    private final BaseMetadataUtils metadataUtils;
    private final VirtualCatalogService virtualCatalogService;
    private final SchemaManager schemaManager;

    public VirtualCatalogRecordDeletedListener(BaseMetadataUtils metadataUtils, VirtualCatalogService virtualCatalogService, SchemaManager schemaManager) {
        this.metadataUtils = metadataUtils;
        this.virtualCatalogService = virtualCatalogService;
        this.schemaManager = schemaManager;
    }

    @Override
    public void onApplicationEvent(RecordDeletedEvent event) {
        String xmlString = event.getPreviousState();
        if (!xmlString.startsWith("<rdf:RDF")) {
            return;
        }

        try {
            Element xml = Xml.loadString(xmlString, false);
            SchemaPlugin schemaPlugin = schemaManager.getSchemaPlugin("dcat-ap");

            if (schemaPlugin == null) {
                Log.error(Geonet.DATA_MANAGER, "Metadata update: Virtual catalog update error - schema plugin not found for dcat-ap");
                return;
            }

            List<Namespace> namespaces = new ArrayList<>(schemaPlugin.getNamespaces());
            // Check if virtual catalog
            if (!Xml.selectBoolean(xml, "dcat:Catalog[not(//dcat:Dataset) and not(//dcat:DataService)]/dct:title", namespaces)) {
                return;
            }

            // remove only if the record is not a draft - portals are configured for published records
            if(!metadataUtils.isMetadataDraft(event.getMdId().intValue())) {
                virtualCatalogService.removePortal(event.getUuid());
            }
        } catch (Exception ex) {
            Log.error(Geonet.DATA_MANAGER, "Metadata update: Virtual catalog update error " + event.getSource(), ex);
        }
    }
}
