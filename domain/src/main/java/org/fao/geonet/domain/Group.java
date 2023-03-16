/*
 * Copyright (C) 2001-2016 Food and Agriculture Organization of the
 * United Nations (FAO-UN), United Nations World Food Programme (WFP)
 * and United Nations Environment Programme (UNEP)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
 *
 * Contact: Jeroen Ticheler - FAO - Viale delle Terme di Caracalla 2,
 * Rome - Italy. email: geonetwork@osgeo.org
 */

package org.fao.geonet.domain;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

import javax.annotation.Nonnull;
import javax.annotation.Nullable;
import javax.persistence.Access;
import javax.persistence.AccessType;
import javax.persistence.Cacheable;
import javax.persistence.CascadeType;
import javax.persistence.CollectionTable;
import javax.persistence.Column;
import javax.persistence.Convert;
import javax.persistence.ElementCollection;
import javax.persistence.Entity;
import javax.persistence.EntityListeners;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.ManyToOne;
import javax.persistence.MapKeyColumn;
import javax.persistence.SequenceGenerator;
import javax.persistence.Table;
import javax.persistence.Transient;
import org.fao.geonet.domain.converter.BooleanToYNConverter;

import org.fao.geonet.entitylistener.GroupEntityListenerManager;

/**
 * An entity representing group of users. Groups in conjunction with {@link Operation}s control what
 * operations users can perform on metadata. <p> For example, user userA is in group groupA and
 * userB is in groupB. It could be that groupA is configured with view operation permission (See
 * {@link OperationAllowed}) then userA could view metadata but userB could not. </p>
 *
 * @author Jesse
 */
@Entity
@Table(name = "Groups")
@Cacheable
@Access(AccessType.PROPERTY)
@EntityListeners(GroupEntityListenerManager.class)
@SequenceGenerator(name = Group.ID_SEQ_NAME, initialValue = 100, allocationSize = 1)
public class Group extends Localized implements Serializable {
    static final String ID_SEQ_NAME = "group_id_seq";

    private int _id;
    private String _name;
    private String _description;
    private String _email;
    private Integer _referrer;
    private String logo;
    private String website;
    private MetadataCategory defaultCategory;
    private List<MetadataCategory> allowedCategories;
    private Boolean enableAllowedCategories;
    private String orgCode;
    private Boolean mdc;

    /**
     * Get the id of the group.
     * <p>
     * This is autogenerated and when a new group is created the group will be
     * assigned a new value.
     *
     * @return the id of the group.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = ID_SEQ_NAME)
    @Column(nullable = false)
    public int getId() {
        return _id;
    }

    /**
     * Get the id of the group. <p> This is autogenerated and when a new group is created the group
     * will be assigned a new value. </p> <p> If you want to update an existing Group then you
     * should set this id to the group you want to update and set the other values to the desired
     * values </p>
     *
     * @param id the id of the group.
     * @return this group object
     */
    public Group setId(int id) {
        this._id = id;
        return this;
    }

    /**
     * Get the basic/default name of the group. This is non-translated and can be used to look up
     * the group like an id can. <p> This is a required property. <p> There is a max length to the
     * name allowed. See the annotation for the length value </p>
     *
     * @return group name
     */
    @Column(nullable = false, length = 255)
    public String getName() {
        return _name;
    }

    /**
     * Set the basic/default name of the group. This is non-translated and can be used to look up
     * the group like an id can. <p> This is a required property. <p> There is a max length to the
     * name allowed. See the annotation on {@link #getName()} for the length value </p>
     */
    public Group setName(String name) {
        this._name = name;
        return this;
    }

    /**
     * Get a description of the group.
     *
     * @return the description.
     */
    @Column(length = 255)
    public String getDescription() {
        return _description;
    }

    /**
     * Set the group description.
     *
     * @param description the description.
     * @return this group object.
     */
    public Group setDescription(String description) {
        this._description = description;
        return this;
    }

    /**
     * Get the email address for the group.
     *
     * @return the email address.
     */
    @Column(length = 128)
    public String getEmail() {
        return _email;
    }

    /**
     * Set the group email address.
     *
     * @param email the email address
     * @return this group object.
     */
    public Group setEmail(String email) {
        this._email = email;
        return this;
    }

    /**
     * TODO UNKNOWN_PROPERTY At the moment the use of this field/column is unknown.
     *
     * @return the referrer
     */
    @Column(nullable = true)
    public Integer getReferrer() {
        return _referrer;
    }

    /**
     * Set the referrer: TODO DOC: it is unknown what the "referrer" is at the moment.
     *
     * @param referrer the referrer.
     */
    public void setReferrer(Integer referrer) {
        this._referrer = referrer;
    }

    @Override
    @ElementCollection(fetch = FetchType.LAZY, targetClass = String.class)
    @CollectionTable(joinColumns = @JoinColumn(name = "idDes"), name = "GroupsDes")
    @MapKeyColumn(name = "langId", length = 5)
    @Column(name = "label", nullable = false, length = 255)
    public Map<String, String> getLabelTranslations() {
        return super.getLabelTranslations();
    }

    @Override
    public String toString() {
        return "Group [_id=" + _id + ", _name=" + _name + ", _email=" + _email
            + "]";
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + _id;
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Group other = (Group) obj;
        if (_id != other._id)
            return false;
        return true;
    }

    @Transient
    public boolean isReserved() {
        return ReservedGroup.isReserved(getId());
    }

    /**
     * Get the logo filename.
     *
     * @return the filename of the logo or null if there is no logo associated with this group.
     */
    @Nullable
    public String getLogo() {
        return logo;
    }

    /**
     * Set the logo filename.
     *
     * @param logo the logo filename
     * @return this entity.
     */
    @Nonnull
    public Group setLogo(@Nullable String logo) {
        this.logo = logo;
        return this;
    }

    /**
     * Return the website url for this group.
     *
     * @return the website url for this group or null if there is none.
     */
    @Nullable
    public String getWebsite() {
        return website;
    }

    /**
     * Set the website url of this group.
     *
     * @param website the website url of this group.
     * @return this group entity object.
     */
    @Nonnull
    public Group setWebsite(@Nullable String website) {
        this.website = website;
        return this;
    }

    /**
     * Default category for this group
     */
    @ManyToOne(cascade = {CascadeType.DETACH,CascadeType.REFRESH,CascadeType.MERGE}, fetch = FetchType.EAGER)
    public MetadataCategory getDefaultCategory() {
        return defaultCategory;
    }

    /**
     * Set the default category of this group
     *
     * @return this group entity object
     */
    public Group setDefaultCategory(MetadataCategory defaultCategory) {
        this.defaultCategory = defaultCategory;
        return this;
    }

    /**
     * Get a list of allowed categories for metadata defined on this group.
     */
    @ManyToMany(fetch = FetchType.EAGER, cascade = {CascadeType.DETACH, CascadeType.PERSIST, CascadeType.REFRESH})
    @JoinTable(name = "group_category",
        joinColumns = {
            @JoinColumn(name = "GROUP_ID", nullable = false, updatable = false)},
        inverseJoinColumns = {
            @JoinColumn(name = "CATEGORY_ID", nullable = false, updatable = false)})
    public List<MetadataCategory> getAllowedCategories() {
        return allowedCategories;
    }

    /**
     *
     * @param allowedCategories
     */
    public void setAllowedCategories(List<MetadataCategory> allowedCategories) {
        this.allowedCategories = allowedCategories;
    }

    /**
     * Should we use the allowedCategories list on this group?
     *
     * @return if false, we allow all categories
     */
    @Column(name = "enableCategoriesRestriction", nullable = true, length = 1, columnDefinition="CHAR(1) DEFAULT 'n'")
    @Convert(converter = BooleanToYNConverter.class)
    public Boolean getEnableAllowedCategories(){
        if (enableAllowedCategories == null) {
            // By default, allow all categories
            this.enableAllowedCategories = false;
        }
        return enableAllowedCategories;
    }

    /**
     * Should we use the enableAllowedCategories list on this group? If false, we allow all
     * categories.
     *
     * @param enableAllowedCategories
     * @return this group entity object
     */
    public Group setEnableAllowedCategories(Boolean enableAllowedCategories) {
        this.enableAllowedCategories = enableAllowedCategories;
        return this;
    }

    @Column(name = "orgcode", nullable = true)
    public String getOrgCode() {
        return orgCode;
    }

    public void setOrgCode(String orgCode) {
        this.orgCode = orgCode;
    }

    @Column(name = "ismdc", nullable = true)
    public Boolean isMdc() {
        return mdc;
    }

    public void setMdc(Boolean mdc) {
        this.mdc = mdc;
    }
}
