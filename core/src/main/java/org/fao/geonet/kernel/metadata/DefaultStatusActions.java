//=============================================================================
//===	Copyright (C) 2001-2023 Food and Agriculture Organization of the
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

package org.fao.geonet.kernel.metadata;

import com.google.common.base.Joiner;
import com.google.common.collect.Sets;
import jeeves.server.UserSession;
import jeeves.server.context.ServiceContext;
import org.apache.commons.lang.StringUtils;
import org.apache.commons.text.StringSubstitutor;
import org.fao.geonet.ApplicationContextHolder;
import org.fao.geonet.constants.Geonet;
import org.fao.geonet.domain.*;
import org.fao.geonet.events.md.MetadataStatusChanged;
import org.fao.geonet.kernel.DataManager;
import org.fao.geonet.kernel.datamanager.*;
import org.fao.geonet.kernel.search.EsSearchManager;
import org.fao.geonet.kernel.setting.SettingManager;
import org.fao.geonet.kernel.setting.Settings;
import org.fao.geonet.repository.*;
import org.fao.geonet.repository.specification.GroupSpecs;
import org.fao.geonet.repository.specification.UserGroupSpecs;
import org.fao.geonet.util.MailUtil;
import org.fao.geonet.util.XslUtil;
import org.fao.geonet.utils.Log;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ConfigurableApplicationContext;

import java.text.MessageFormat;
import java.util.*;
import java.util.stream.Collectors;

import static org.fao.geonet.kernel.setting.Settings.SYSTEM_FEEDBACK_EMAIL;

public class DefaultStatusActions implements StatusActions {

    protected ServiceContext context;
    protected String language;
    protected DataManager dm;
    @Autowired
    protected IMetadataUtils metadataUtils;
    protected String siteUrl;
    protected String siteName;
    protected UserSession session;
    protected boolean emailNotes = true;
    private String replyTo;
    private String replyToDescr;
    private StatusValueRepository statusValueRepository;
    protected IMetadataStatus metadataStatusManager;
    private IMetadataValidator metadataValidator;
    private IMetadataUtils metadataRepository;
    private IMetadataManager metadataManager;
    private IMetadataOperations metadataOperations;
    private EsSearchManager searchManager;


    /**
     * Constructor.
     */
    public DefaultStatusActions() {
    }

    /**
     * Initializes the StatusActions class with external info from GeoNetwork.
     */
    public void init(ServiceContext context) throws Exception {

        this.context = context;
        ApplicationContext applicationContext = ApplicationContextHolder.get();
        this.statusValueRepository = applicationContext.getBean(StatusValueRepository.class);
        this.metadataUtils = applicationContext.getBean(IMetadataUtils.class);
        this.language = context.getLanguage();

        SettingManager sm = applicationContext.getBean(SettingManager.class);

        siteName = sm.getSiteName();
        String from = sm.getValue(SYSTEM_FEEDBACK_EMAIL);

        if (from == null || from.length() == 0) {
            context.error("Mail feedback address not configured, email notifications won't be sent.");
            emailNotes = false;
        }

        session = context.getUserSession();
        replyTo = session.getEmailAddr();
        if (replyTo != null) {
            replyToDescr = session.getName() + " " + session.getSurname();
        } else {
            replyTo = from;
            replyToDescr = siteName;
        }

        dm = applicationContext.getBean(DataManager.class);
        metadataStatusManager = applicationContext.getBean(IMetadataStatus.class);
        searchManager = applicationContext.getBean(EsSearchManager.class);
        siteUrl = sm.getSiteURL(context);

        metadataValidator = context.getBean(IMetadataValidator.class);
        metadataOperations = context.getBean(IMetadataOperations.class);
        metadataManager = context.getBean(IMetadataManager.class);
        metadataRepository = context.getBean(IMetadataUtils.class);

    }

    /**
     * Called when a record is edited to set/reset status.
     *
     * @param id        The metadata id that has been edited.
     * @param minorEdit If true then the edit was a minor edit.
     */
    public void onEdit(int id, boolean minorEdit) throws Exception {
        if (Log.isTraceEnabled(Geonet.DATA_MANAGER)) {
            Log.trace(Geonet.DATA_MANAGER, "DefaultStatusActions.onEdit(" + id + ", " + minorEdit + ") with status "
                + dm.getCurrentStatus(id));
        }
        // VL specific
        if (!minorEdit && !dm.getCurrentStatus(id).equals(StatusValue.Status.DRAFT)) {
            ResourceBundle messages = ResourceBundle.getBundle("org.fao.geonet.api.Messages",
                new Locale(this.language));
            String changeMessage = String.format(messages.getString("status_email_text"), replyToDescr, replyTo, id);
            Log.trace(Geonet.DATA_MANAGER, "Set DRAFT to current record with id " + id);
            dm.setStatus(context, id, Integer.parseInt(StatusValue.Status.DRAFT), new ISODate(), changeMessage);
        }
    }

    public void cancelEditStatus(ServiceContext context, int id) throws Exception {
        String statusBeforeAnyChanges = (String) session.getProperty(Geonet.Session.METADATA_STATUS_BEFORE_ANY_CHANGES + id);
        if (statusBeforeAnyChanges != null) {
            ResourceBundle messages = ResourceBundle.getBundle("org.fao.geonet.api.Messages",
                new Locale(this.language));
            String changeMessage = String.format(messages.getString("status_cancel_email_text"), replyToDescr, replyTo, id);
            dm.setStatus(context, id, Integer.parseInt(statusBeforeAnyChanges), new ISODate(), changeMessage);
        } else {
            if (Log.isDebugEnabled(Geonet.EDITOR_SESSION)) {
                Log.debug(Geonet.EDITOR_SESSION, " > no status to cancel for record " + id
                    + ". Original record status was null. Use starteditingsession to.");
            }
        }
    }

    /**
     * Called when a record status is added.
     *
     * @param listOfStatus
     * @return
     * @throws Exception
     */
    public Map<Integer, StatusChangeType> onStatusChange(List<MetadataStatus> listOfStatus, boolean updateIndex) throws Exception {

        if (listOfStatus.stream().map(MetadataStatus::getMetadataId).distinct().count() != listOfStatus.size()) {
            throw new IllegalArgumentException("Multiple status update received on the same metadata");
        }

        Map<Integer, StatusChangeType> results = new HashMap<>();

        // process the metadata records to set status
        for (MetadataStatus status : listOfStatus) {
            MetadataStatus currentStatus = dm.getStatus(status.getMetadataId());
            String currentStatusId = (currentStatus != null) ?
                String.valueOf(currentStatus.getStatusValue().getId()) : "";


            String statusId = status.getStatusValue().getId() + "";
            Set<Integer> listOfId = new HashSet<>(1);
            listOfId.add(status.getMetadataId());

            // For the workflow, if the status is already set to value
            // of status then do nothing. This does not apply to task and event.
            if (status.getStatusValue().getType().equals(StatusValueType.workflow) &&
                (statusId).equals(currentStatusId)) {
                if (context.isDebugEnabled())
                    context.debug(String.format("Metadata %s already has status %s ",
                        status.getMetadataId(), status.getStatusValue().getId()));
                results.put(status.getMetadataId(), StatusChangeType.UNCHANGED);
                continue;
            }

            // if not possible to go from one status to the other, don't continue
            AbstractMetadata metadata = metadataRepository.findOne(status.getMetadataId());
            if (!isStatusChangePossible(session.getProfile(), metadata, currentStatusId, statusId)) {
                results.put(status.getMetadataId(), StatusChangeType.UNCHANGED);
                continue;
            }

            // debug output if necessary
            if (context.isDebugEnabled())
                context.debug("Change status of metadata with id " + status.getMetadataId() + " from " + currentStatusId + " to " + statusId);

            // we know we are allowed to do the change, apply any side effects
            boolean deleted = applyStatusChange(status.getMetadataId(), status, statusId, metadata, updateIndex);

            // inform content reviewers if the status is submitted
            try {
                vlNotify(vlGetUserToNotify(currentStatus, status, metadata), currentStatus, status);
            } catch (Exception e) {
                String msg = String.format(
                    "Failed to send notification on status change for metadata %s with status %s. Error is: %s",
                    status.getMetadataId(), status.getStatusValue().getId(), e.getMessage());
                Log.error(Geonet.DATA_MANAGER, msg);
                context.warning(msg);
            }

            if (deleted) {
                results.put(status.getMetadataId(), StatusChangeType.DELETED);
            } else {
                results.put(status.getMetadataId(), StatusChangeType.UPDATED);
            }
            // throw events
            Log.trace(Geonet.DATA_MANAGER, "Throw workflow events.");
            for (Integer mid : listOfId) {
                if (results.get(mid) != StatusChangeType.DELETED) {
                    Log.debug(Geonet.DATA_MANAGER, "  > Status changed for record (" + mid + ") to status " + status);
                    context.getApplicationContext().publishEvent(new MetadataStatusChanged(
                        metadataUtils.findOne(mid),
                        status.getStatusValue(), status.getChangeMessage(),
                        status.getUserId()
                    ));
                }
            }
        }

        return results;
    }

    /**
     * Placeholder to apply any side effects.
     * eg. if APPROVED, publish a record,
     * if RETIRED, unpublish or delete the record.
     */
    private boolean applyStatusChange(int metadataId, MetadataStatus status, String toStatusId, AbstractMetadata metadata, boolean updateIndex) throws Exception {
        // in the case of rejected for retired/removed: fall back to the previous status
        boolean deleted = false;
        if (Sets.newHashSet(StatusValue.Status.REJECTED_FOR_RETIRED, StatusValue.Status.REJECTED_FOR_REMOVED)
                .contains(toStatusId)) {
            MetadataStatus previousStatus = metadataStatusManager.getPreviousStatus(metadataId);
            // only if we actually have a previous state
            if (previousStatus != null) {
                StatusValue statusValue = previousStatus.getStatusValue();

                MetadataStatus metadataStatus = new MetadataStatus();
                metadataStatus.setUuid(status.getUuid());
                metadataStatus.setStatusValue(statusValue);
                metadataStatus.setChangeDate(new ISODate());
                metadataStatus.setUserId(session.getUserIdAsInt());
                metadataStatus.setMetadataId(status.getMetadataId());
                metadataStatus.setChangeMessage(status.getChangeMessage());

                metadataStatusManager.setStatusExt(metadataStatus, updateIndex);
            }
        }
        // if we're approving, automatically publish
        else if (toStatusId.equals(StatusValue.Status.APPROVED)) {
            // if we have a draft copy that has a modified groupowner we need to take that into account as well
            if(metadata instanceof MetadataDraft) {
                MetadataDraft draft = (MetadataDraft) metadata;
                Metadata approved = (Metadata) metadataRepository.findOne(draft.getApprovedVersion().getId());
                if(!draft.getSourceInfo().getGroupOwner().equals(approved.getSourceInfo().getGroupOwner())) {
                    useDraftGroupOwner(draft, approved);
                }
            }
            // publish
            setAllOperations(String.valueOf(status.getMetadataId()));
        }
        // if we're rejecting, automatically unpublish
        else if (toStatusId.equals(StatusValue.Status.RETIRED)) {
            unsetAllOperations(metadataId);
        }
        // if we're rejecting, automatically unpublish
        else if (toStatusId.equals(StatusValue.Status.REMOVED)) {
            metadataManager.purgeMetadata(context, String.valueOf(status.getMetadataId()), true);
            deleted = true;
        }

        if (!deleted) {
            metadataStatusManager.setStatusExt(status, updateIndex);
        }
        return deleted;
    }

    /**
     * Set the group owner of the approved record to the draft's one.
     * @param draft the draft that has the new owner
     * @param approved the approved version whose owner needs to be overwritten
     */
    private void useDraftGroupOwner(MetadataDraft draft, Metadata approved) {
        Integer oldGroupOwner = approved.getSourceInfo().getGroupOwner();
        Integer newGroupOwner = draft.getSourceInfo().getGroupOwner();

        metadataOperations.getAllOperations(approved.getId())
            .stream()
            .filter(op -> op.getId().getGroupId() == oldGroupOwner)
            .forEach(op -> {
                try {
                    // remove the old privilege for the old group owner
                    metadataOperations.forceUnsetOperation(context, approved.getId(), oldGroupOwner, op.getId().getOperationId());
                    // add the same privilege, but for the new group owner
                    metadataOperations.forceSetOperation(context, approved.getId(), newGroupOwner, op.getId().getOperationId());
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            });

        // set the new owner
        approved.getSourceInfo().setGroupOwner(newGroupOwner);
    }

    /**
     * Customised version of the notify function. Sends out a custom HTML mail to interested users.
     *
     * @param userToNotify the users that will be notified by the change
     * @param currentStatus the current status of the record
     * @param status the new status of the record
     */
    protected void vlNotify(List<User> userToNotify, MetadataStatus currentStatus, MetadataStatus status) {
        // validate
        if ((userToNotify == null) || userToNotify.isEmpty()) {
            return;
        }

        // prerequisites
        ApplicationContext applicationContext = ApplicationContextHolder.get();
        GroupRepository groupRepository = context.getBean(GroupRepository.class);
        SettingManager sm = applicationContext.getBean(SettingManager.class);
        SourceRepository sourceRepository = context.getBean(SourceRepository.class);
        UserGroupRepository userGroupRepository = context.getBean(UserGroupRepository.class);
        UserRepository userRepository = context.getBean(UserRepository.class);
        IMetadataUtils metadataRepository = ApplicationContextHolder.get().getBean(IMetadataUtils.class);
        ResourceBundle messages = ResourceBundle.getBundle("org.fao.geonet.api.Messages", new Locale(this.language));
        AbstractMetadata metadata = metadataRepository.findOne(status.getMetadataId());

        // gather required data
        String statusName = getTranslatedStatusName(status.getStatusValue().getId());
        String currentStatusName = getTranslatedStatusName(currentStatus.getStatusValue().getId());
        String subjectTemplate = messages.getString("vl_status_change_email_subject");
        String textTemplate = messages.getString("vl_status_change_email_text");
        String recordTypeDraft = messages.getString("vl_record_type_draft");
        String recordTypeNonDraft = messages.getString("vl_record_type_nondraft");
        // what groups does our user belong to?
        List<UserGroup> userGroups = userGroupRepository.findAll(
            UserGroupSpecs.hasUserId(Integer.parseInt(context.getUserSession().getUserId())));
        // we want to show the group the user belongs to: we want the non-datapublicatie one
        Optional<UserGroup> groupOfUser = userGroups
            .stream()
            .filter((g) -> !g.getGroup().getVlType().equals("datapublicatie"))
            .findFirst();
        boolean isAdmin = session.getProfile().equals(Profile.Administrator);
        String metadataUrl = metadataUtils.getDefaultUrl(metadata.getUuid(), this.language);
        VlEnvironment environment = getEnvironment(sm.getNodeURL());
        boolean isDraft = metadata instanceof MetadataDraft;
        String userFullName = String.join(" ", context.getUserSession().getName(), context.getUserSession().getSurname());
        Optional<Group> groupOwner = groupRepository.findById(metadata.getSourceInfo().getGroupOwner());
        String dpPrefix = groupOwner.filter(g -> StringUtils.equals(g.getVlType(), "datapublicatie")).isPresent() ? "Datapublicatie " : "";
        String statusChangeReason = status.getChangeMessage().trim();

        String metadataTitle = XslUtil.getIndexField(null, metadata.getUuid(), "resourceTitleObject", this.language);

        // gather parameters for the email
        // top-level, the mail is composed of 'sections', these need to be replaced first
        Map<String, String> sections = new HashMap<>();
        if (isAdmin) {
            sections.put("section-action", messages.getString("vl_status_change_email_text_action_admin"));
        } else {
            sections.put("section-action", messages.getString("vl_status_change_email_text_action_user"));
        }
        if (status.getStatusValue().getId() == Integer.parseInt(StatusValue.Status.REMOVED)) {
            sections.put("section-link", messages.getString("vl_status_change_email_text_link_removed"));
        } else {
            sections.put("section-link", messages.getString("vl_status_change_email_text_link_present"));
        }
        if(statusChangeReason.isBlank()) {
            sections.put("section-reason", messages.getString("vl_status_change_email_text_reason_absent"));
        } else {
            sections.put("section-reason", messages.getString("vl_status_change_email_text_reason_present"));
        }
        // then, replace the bottom-level parameters
        Map<String, String> values = new HashMap<>();
        values.put("environment", environment.getLongText());
        values.put("userFullName", userFullName);
        values.put("recordTitle", metadataTitle);
        values.put("previousStatus", currentStatusName);
        values.put("newStatus", statusName);
        values.put("organisationName", (groupOfUser.map(g -> g.getGroup().getName())).orElse("<error>"));
        values.put("recordUrl", metadataUrl);
        values.put("statusChangeReason", statusChangeReason);
        values.put("artifact", environment.getArtifactName());
        values.put("recordType", isDraft ? recordTypeDraft : recordTypeNonDraft);
        values.put("datapublicatiePrefix", dpPrefix);

        // format the mail body
        //  - top level replacements
        String message = StringSubstitutor.replace(textTemplate, sections);
        //  - value replacements
        message = StringSubstitutor.replace(message, values);

        // format the subject matter
        String subject = StringSubstitutor.replace(subjectTemplate, values);

        // mix in index fields (not sure we use these presently, but keeping it in here for reference)
        subject = MailUtil.compileMessageWithIndexFields(subject, metadata.getUuid(), this.language);
        message = MailUtil.compileMessageWithIndexFields(message, metadata.getUuid(), this.language);

        // send out the mails
        for (User user : userToNotify) {
            String email = user.getEmail();
            if(MailUtil.isValidMailAddress(email)) {
                sendEmail(user.getEmail(), subject, message);
            }
        }
    }

    private static VlEnvironment getEnvironment(String nodeUrl) {
        if (nodeUrl.contains("metadata.vlaanderen.be")) {
            return VlEnvironment.PRD;
        } else if (nodeUrl.contains("metadata.beta-vlaanderen.be")) {
            return VlEnvironment.BET;
        } else if (nodeUrl.contains("metadata.dev-vlaanderen.be")) {
            return VlEnvironment.DEV;
        } else return VlEnvironment.LOC;
    }

    private enum VlEnvironment {
        LOC("Local"), DEV("Dev"), BET("Beta"), PRD("Productie");

        private final String longText;

        VlEnvironment(String longText) {
            this.longText = longText;
        }

        public String getLongText() {
            return longText;
        }

        public String getArtifactName() {
            return "Metadata Vlaanderen" + ((this != PRD) ? " (" + longText + ")" : "");
        }
    }


    /**
     * Send email to a list of users. The list of users is defined based on the
     * notification level of the status. See {@link StatusValueNotificationLevel}.
     *
     * @param userToNotify
     * @param status
     * @throws Exception
     */
    protected void notify(List<User> userToNotify, MetadataStatus status) throws Exception {
        if ((userToNotify == null) || userToNotify.isEmpty()) {
            return;
        }

        ResourceBundle messages = ResourceBundle.getBundle("org.fao.geonet.api.Messages", new Locale(this.language));

        String translatedStatusName = getTranslatedStatusName(status.getStatusValue().getId());
        // TODO: Refactor to allow custom messages based on the type of status
        String subjectTemplate = "";
        try {
            subjectTemplate = messages
                .getString("status_change_" + status.getStatusValue().getName() + "_email_subject");
        } catch (MissingResourceException e) {
            subjectTemplate = messages.getString("status_change_default_email_subject");
        }
        String subject = MessageFormat.format(subjectTemplate, siteName, translatedStatusName, replyToDescr // Author of the change
        );

        Set<Integer> listOfId = new HashSet<>(1);
        listOfId.add(status.getMetadataId());

        String textTemplate = "";
        try {
            textTemplate = messages.getString("status_change_" + status.getStatusValue().getName() + "_email_text");
        } catch (MissingResourceException e) {
            textTemplate = messages.getString("status_change_default_email_text");
        }

        // Replace link in message
        ApplicationContext applicationContext = ApplicationContextHolder.get();
        SettingManager sm = applicationContext.getBean(SettingManager.class);
        textTemplate = textTemplate.replace("{{link}}", sm.getNodeURL()+ "api/records/'{{'index:uuid'}}'");

        UserRepository userRepository = context.getBean(UserRepository.class);
        User owner = userRepository.findById(status.getOwner()).orElse(null);

        IMetadataUtils metadataRepository = ApplicationContextHolder.get().getBean(IMetadataUtils.class);
        AbstractMetadata metadata = metadataRepository.findOne(status.getMetadataId());

        String metadataUrl = metadataUtils.getDefaultUrl(metadata.getUuid(), this.language);

        String message = MessageFormat.format(textTemplate, replyToDescr, // Author of the change
            status.getChangeMessage(), translatedStatusName, status.getChangeDate(), status.getDueDate(),
            status.getCloseDate(),
            owner == null ? "" : Joiner.on(" ").skipNulls().join(owner.getName(), owner.getSurname()),
            metadataUrl);


        subject = MailUtil.compileMessageWithIndexFields(subject, metadata.getUuid(), this.language);
        message = MailUtil.compileMessageWithIndexFields(message, metadata.getUuid(), this.language);
        for (User user : userToNotify) {
            String salutation = Joiner.on(" ").skipNulls().join(user.getName(), user.getSurname());
            //If we have a salutation then end it with a ","
            if (StringUtils.isEmpty(salutation)) {
                salutation = "";
            } else {
                salutation += ",\n\n";
            }
            sendEmail(user.getEmail(), subject, salutation + message);
        }
    }

    /**
     * Based on the status notification level defined in the database collect the
     * list of users to notify.
     *
     * @param status
     * @return
     */
    protected List<User> getUserToNotify(MetadataStatus status) {
        StatusValueNotificationLevel notificationLevel = status.getStatusValue().getNotificationLevel();

        // If new status is DRAFT and previous status is not SUBMITTED (which means a rejection),
        // ignore notifications as the DRAFT status is used also when creating the working copy.
        // We don't want to notify when creating a working copy.
        if (status.getStatusValue().getId() == Integer.parseInt(StatusValue.Status.DRAFT) &&
            ((StringUtils.isEmpty(status.getPreviousState())) ||
                (Integer.parseInt(status.getPreviousState()) != Integer.parseInt(StatusValue.Status.SUBMITTED)))) {
                return new ArrayList<>();
        }

        // TODO: Status does not provide batch update
        // So taking care of one record at a time.
        // Currently the code could notify a mix of reviewers
        // if records are not in the same groups. To be improved.
        Set<Integer> listOfId = new HashSet<>(1);
        listOfId.add(status.getMetadataId());
        return getUserToNotify(notificationLevel, listOfId, status.getOwner());
    }

    public static List<User> vlGetUserToNotify(MetadataStatus currentStatus, MetadataStatus status, AbstractMetadata metadata) {
        StatusValueNotificationLevel notificationLevel = status.getStatusValue().getNotificationLevel();
        UserRepository userRepository = ApplicationContextHolder.get().getBean(UserRepository.class);
        UserGroupRepository userGroupRepository = ApplicationContextHolder.get().getBean(UserGroupRepository.class);
        GroupRepository groupRepository = ApplicationContextHolder.get().getBean(GroupRepository.class);

        // If new status is DRAFT and previous status is not SUBMITTED (which means a rejection),
        // ignore notifications as the DRAFT status is used also when creating the working copy.
        // We don't want to notify when creating a working copy.
        if (status.getStatusValue().getId() == Integer.parseInt(StatusValue.Status.DRAFT) &&
            ((StringUtils.isEmpty(status.getPreviousState())) ||
                (Integer.parseInt(status.getPreviousState()) != Integer.parseInt(StatusValue.Status.SUBMITTED)))) {
            Log.debug(Geonet.DATA_MANAGER, "DefaultStatusActions.vlGetUserToNotify(not sending, creating a working copy)");
            return new ArrayList<>();
        }

        // get the record owner group of the record
        Optional<Group> recordOwnerGroup = groupRepository.findById(metadata.getSourceInfo().getGroupOwner());
        if (recordOwnerGroup.isEmpty()) {
            // if we have no record owner group we cannot determine our next action - do nothing
            Log.debug(Geonet.DATA_MANAGER, "DefaultStatusActions.vlGetUserToNotify(not sending, record has no groupOwner)");
            return new ArrayList<>();
        }
        boolean isDatapublicatie = StringUtils.equals(recordOwnerGroup.get().getVlType(), "datapublicatie");
        // all users from the record owner group
        List<UserGroup> recordOwnerGroupUsers = userGroupRepository.findAll(UserGroupSpecs.hasGroupId(metadata.getSourceInfo().getGroupOwner()));
        // all admins of Digitaal Vlaanderen
        Group digitaalVlaanderen = groupRepository.findByOrgCodeAndVlType("OVO002949", "metadatavlaanderen");
        List<UserGroup> digitaalVlaanderenAdmins = userGroupRepository
                .findAll(UserGroupSpecs.hasGroupId(digitaalVlaanderen.getId()))
                .stream()
                .filter(u -> u.getProfile() == Profile.UserAdmin)
                .collect(Collectors.toList());


        Set<Integer> userIdsToNotify = new HashSet<>();
        userIdsToNotify.addAll(recordOwnerGroupUsers.stream().map(UserGroup::getUser).map(User::getId).collect(Collectors.toList()));
        if(isDatapublicatie) {
            userIdsToNotify.addAll(digitaalVlaanderenAdmins.stream().map(UserGroup::getUser).map(User::getId).collect(Collectors.toList()));
        } else {
            String statusId = String.valueOf(status.getStatusValue().getId());
            if(Sets.newHashSet(StatusValue.Status.APPROVED,
                StatusValue.Status.RETIRED,
                StatusValue.Status.REMOVED).contains(statusId)) {
                userIdsToNotify.addAll(
                    digitaalVlaanderenAdmins.stream()
                        .map(UserGroup::getUser)
                        .map(User::getId)
                        .collect(Collectors.toList()));
            }
        }
        return userRepository.findAllById(userIdsToNotify);
    }

    public static List<User> getUserToNotify(StatusValueNotificationLevel notificationLevel, Set<Integer> recordIds, Integer ownerId) {
        UserRepository userRepository = ApplicationContextHolder.get().getBean(UserRepository.class);
        List<User> users = new ArrayList<>();

        if (notificationLevel != null) {
            if (notificationLevel == StatusValueNotificationLevel.statusUserOwner) {
                Optional<User> owner = userRepository.findById(ownerId);

                if (owner.isPresent()) {
                    users.add(owner.get());
                }
            } else if (notificationLevel == StatusValueNotificationLevel.recordProfileReviewer) {
                List<Pair<Integer, User>> results = userRepository.findAllByGroupOwnerNameAndProfile(recordIds, Profile.Reviewer);
                Collections.sort(results, Comparator.comparing(s -> s.two().getName()));
                for (Pair<Integer, User> p : results) {
                    users.add(p.two());
                }
            } else if (notificationLevel == StatusValueNotificationLevel.recordUserAuthor) {
                Iterable<Metadata> records = ApplicationContextHolder.get().getBean(MetadataRepository.class).findAllById(recordIds);
                for (Metadata r : records) {
                    Optional<User> owner = userRepository.findById(r.getSourceInfo().getOwner());

                    if (owner.isPresent()) {
                        users.add(owner.get());
                    }
                }

                // Check metadata drafts
                Iterable<MetadataDraft> recordsDraft = ApplicationContextHolder.get().getBean(MetadataDraftRepository.class).findAllById(recordIds);

                for (MetadataDraft r : recordsDraft) {
                    Optional<User> owner = userRepository.findById(r.getSourceInfo().getOwner());

                    if (owner.isPresent()) {
                        users.add(owner.get());
                    }
                }
            } else if (notificationLevel.name().startsWith("catalogueProfile")) {
                String profileId = notificationLevel.name().replace("catalogueProfile", "");
                Profile profile = Profile.findProfileIgnoreCase(profileId);
                users = userRepository.findAllByProfile(profile);
            } else if (notificationLevel == StatusValueNotificationLevel.catalogueAdministrator) {
                SettingManager settingManager = ApplicationContextHolder.get().getBean(SettingManager.class);
                String adminEmail = settingManager.getValue(SYSTEM_FEEDBACK_EMAIL);
                if (StringUtils.isNotEmpty(adminEmail)) {
                    Set<String> emails = new HashSet<>(1);
                    emails.add(adminEmail);
                    User catalogueAdmin = new User().setEmailAddresses(emails);
                    users.add(catalogueAdmin);
                }
            }
        }
        return users;
    }

    public static List<Group> getGroupToNotify(StatusValueNotificationLevel notificationLevel, List<String> groupNames) {
        GroupRepository groupRepository = ApplicationContextHolder.get().getBean(GroupRepository.class);
        List<Group> groups = new ArrayList<>();

        if ((notificationLevel != null) && (notificationLevel == StatusValueNotificationLevel.recordGroupEmail)) {
            groups = groupRepository.findAll(GroupSpecs.inGroupNames(groupNames));
        }

        return groups;
    }


    /**
     * Unset all operations on 'All' Group. Used when status
     * changes from approved to something else.
     *
     * @param mdId The metadata id to unset privileges on
     */
    protected void unsetAllOperations(int mdId) throws Exception {
        Log.trace(Geonet.DATA_MANAGER, "DefaultStatusActions.unsetAllOperations(" + mdId + ")");

        int allGroup = 1;
        for (ReservedOperation op : ReservedOperation.values()) {
            metadataOperations.forceUnsetOperation(context, mdId, allGroup, op.getId());
        }
    }

    /**
     * Set all operations on 'All' Group. Used when status changes to approved.
     *
     * @param mdId The metadata id to set privileges on
     */
    protected void setAllOperations(String mdId) throws Exception {
        String allGroup = "1";
        metadataOperations.setOperation(context, mdId, allGroup, ReservedOperation.view);
        metadataOperations.setOperation(context, mdId, allGroup, ReservedOperation.view);
        metadataOperations.setOperation(context, mdId, allGroup, ReservedOperation.download);
        metadataOperations.setOperation(context, mdId, allGroup, ReservedOperation.notify);
        metadataOperations.setOperation(context, mdId, allGroup, ReservedOperation.dynamic);
        metadataOperations.setOperation(context, mdId, allGroup, ReservedOperation.featured);
    }

    private String getTranslatedStatusName(int statusValueId) {
        String translatedStatusName = "";
        StatusValue s = statusValueRepository.findOneById(statusValueId);
        if (s == null) {
            translatedStatusName = statusValueId
                + " (Status not found in database translation table. Check the content of the StatusValueDes table.)";
        } else {
            translatedStatusName = s.getLabel(this.language);
        }
        return translatedStatusName;
    }

    /**
     * Send the email message about change of status on a group of metadata records.
     *
     * @param sendTo  The recipient email address
     * @param subject Subject to be used for email notices
     * @param message Text of the mail
     */
    protected void sendEmail(String sendTo, String subject, String message) {
        Log.debug(Geonet.DATA_MANAGER, "DefaultStatusActions.sendEmail(" + sendTo + ")");
        if (!emailNotes) {
            context.info("Would send email \nTo: " + sendTo + "\nSubject: " + subject + "\n Message:\n" + message);
        } else {
            ApplicationContext applicationContext = ApplicationContextHolder.get();
            SettingManager sm = applicationContext.getBean(SettingManager.class);
            // Doesn't make sense go further without any mailserver set...
            if (StringUtils.isNotBlank(sm.getValue(Settings.SYSTEM_FEEDBACK_MAILSERVER_HOST))) {
                List<String> to = new ArrayList<>();
                to.add(sendTo);
                // vl: we send HTML messages, not plain text
                MailUtil.sendMail(to, subject, null, message, sm, replyTo, replyToDescr);
            }
        }
    }

    /**
     * Calculate the from-to relations between status values, as applicable to an editor.
     * <p>
     * VL modification.
     *
     * @return a map of status to the possible follow-up statuses
     */
    private Map<String, Set<String>> getEditorFlow() {
        HashMap<String, Set<String>> result = new HashMap<>();
        // initialise the map
        Sets.newHashSet(
                StatusValue.Status.DRAFT,
                StatusValue.Status.APPROVED,
                StatusValue.Status.RETIRED,
                StatusValue.Status.SUBMITTED,
                StatusValue.Status.REJECTED,
                StatusValue.Status.APPROVED_FOR_PUBLISHED,
                StatusValue.Status.SUBMITTED_FOR_RETIRED,
                StatusValue.Status.SUBMITTED_FOR_REMOVED,
                StatusValue.Status.REMOVED,
                StatusValue.Status.REJECTED_FOR_RETIRED,
                StatusValue.Status.REJECTED_FOR_REMOVED
        ).forEach(s -> result.put(s, new HashSet<>()));

        // set the values for editor
        result.get(StatusValue.Status.DRAFT).addAll(Sets.newHashSet(
                StatusValue.Status.REMOVED,
                StatusValue.Status.SUBMITTED
        ));
        result.get(StatusValue.Status.SUBMITTED).addAll(Sets.newHashSet(
                StatusValue.Status.REMOVED
        ));
        result.get(StatusValue.Status.REJECTED).addAll(Sets.newHashSet(
                StatusValue.Status.SUBMITTED,
                StatusValue.Status.REMOVED
        ));
        result.get(StatusValue.Status.APPROVED).addAll(Sets.newHashSet(
                StatusValue.Status.SUBMITTED_FOR_RETIRED,
                StatusValue.Status.SUBMITTED_FOR_REMOVED
        ));
        result.get(StatusValue.Status.SUBMITTED_FOR_RETIRED).addAll(Sets.newHashSet(
            StatusValue.Status.REJECTED_FOR_RETIRED
        ));
        result.get(StatusValue.Status.RETIRED).addAll(Sets.newHashSet(
                StatusValue.Status.SUBMITTED_FOR_REMOVED
        ));
        result.get(StatusValue.Status.SUBMITTED_FOR_REMOVED).addAll(Sets.newHashSet(
                StatusValue.Status.REJECTED_FOR_REMOVED
        ));
        return result;
    }

    /**
     * Calculate the from-to relations between status values, as applicable to a reviewer.
     * This adds upon the capabilities of an editor.
     * <p>
     * VL modification.
     *
     * @return a map of status to the possible follow-up statuses
     */
    private Map<String, Set<String>> getReviewerFlow() {
        Map<String, Set<String>> result = getEditorFlow();
        result.get(StatusValue.Status.DRAFT).addAll(Sets.newHashSet(
                StatusValue.Status.APPROVED_FOR_PUBLISHED,
                StatusValue.Status.APPROVED
        ));
        result.get(StatusValue.Status.SUBMITTED).addAll(Sets.newHashSet(
                StatusValue.Status.REJECTED,
                StatusValue.Status.APPROVED_FOR_PUBLISHED,
                StatusValue.Status.APPROVED
        ));
        result.get(StatusValue.Status.APPROVED_FOR_PUBLISHED).addAll(Sets.newHashSet(
                StatusValue.Status.SUBMITTED,
                StatusValue.Status.REJECTED,
                StatusValue.Status.APPROVED,
                StatusValue.Status.REMOVED
        ));
        result.get(StatusValue.Status.APPROVED).addAll(Sets.newHashSet(
                StatusValue.Status.RETIRED,
                StatusValue.Status.REMOVED
        ));
        result.get(StatusValue.Status.SUBMITTED_FOR_RETIRED).addAll(Sets.newHashSet(
                StatusValue.Status.RETIRED,
                StatusValue.Status.REMOVED
        ));
        result.get(StatusValue.Status.RETIRED).addAll(Sets.newHashSet(
                StatusValue.Status.APPROVED,
                StatusValue.Status.REMOVED
        ));
        result.get(StatusValue.Status.REJECTED_FOR_RETIRED).addAll(Sets.newHashSet(
                StatusValue.Status.APPROVED
        ));
        result.get(StatusValue.Status.SUBMITTED_FOR_REMOVED).addAll(Sets.newHashSet(
                StatusValue.Status.APPROVED,
                StatusValue.Status.RETIRED,
                StatusValue.Status.REMOVED
        ));
        return result;
    }

    /**
     * Calculate the from-to relations between status values, as applicable to an admin.
     * This adds upon the capabilities of a reviewer.
     * <p>
     * VL modification.
     *
     * @return a map of status to the possible follow-up statuses
     */
    private Map<String, Set<String>> getAdminFlow() {
        return getReviewerFlow();
    }

    /**
     * Test whether a given status change for a given role is allowed or not.
     * <p>
     * VL modification.
     *
     * @param profile    the role that tries to execute the status change
     * @param fromStatus the status from which we start
     * @param toStatus   the status to which we'd like to change
     * @return whether the change is allowed
     */
    private boolean isStatusChangePossible(Profile profile, AbstractMetadata metadata, String fromStatus, String toStatus) throws Exception {
        // special case: enabling the workflow sets the initial 'draft' status
        if (StringUtils.isEmpty(fromStatus) && toStatus.equals(StatusValue.Status.DRAFT))
            return true;
        // figure out whether we can switch from status to status, depending on the profile
        Set<String> toProfiles = new HashSet<>();
        switch (profile) {
            case Editor:
                toProfiles = getEditorFlow().get(fromStatus);
                break;
            case Administrator:
                toProfiles = getAdminFlow().get(fromStatus);
                break;
            case Reviewer:
                toProfiles = getReviewerFlow().get(fromStatus);
                break;
        }
        return toProfiles != null && toProfiles.contains(toStatus);
    }
}
