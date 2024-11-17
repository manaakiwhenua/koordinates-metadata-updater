# Merging dictionaries
# Python 3.9+ syntax using dictionary union operator

import os
import xml.etree.ElementTree as ET
import openpyxl


tree = ET.parse(file_path)
root = tree.getroot()
namespaces = {
    'gmd': 'http://www.isotc211.org/2005/gmd',
    'gco': 'http://www.isotc211.org/2005/gco',
    'srv': 'http://www.isotc211.org/2005/srv',
    'gml': 'http://www.opengis.net/gml',
    'xlink': 'http://www.w3.org/1999/xlink'
}

def get_text(path):
    found = root.find(path, namespaces)
    return found.text if found is not None else ''


d1 = {
    # Metadata Information
    'fileIdentifier_CharacterString': get_text('./gmd:fileIdentifier/gco:CharacterString'),
    'language_LanguageCode': get_text('./gmd:language/gmd:LanguageCode'),
    'characterSet_MD_CharacterSetCode': get_text('./gmd:characterSet/gmd:MD_CharacterSetCode'),
    'hierarchyLevel_MD_ScopeCode': get_text('./gmd:hierarchyLevel/gmd:MD_ScopeCode'),
    'hierarchyLevelName_CharacterString': get_text('./gmd:hierarchyLevelName/gco:CharacterString'),
    'dateStamp_Date': get_text('./gmd:dateStamp/gco:Date'),
    'metadataStandardName_CharacterString': get_text('./gmd:metadataStandardName/gco:CharacterString'),
    'metadataStandardVersion_CharacterString': get_text('./gmd:metadataStandardVersion/gco:CharacterString'),

    # Contact Information
    'contact_CI_ResponsibleParty_individualName': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
    'contact_CI_ResponsibleParty_organisationName': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
    'contact_CI_ResponsibleParty_positionName': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
    'contact_CI_ResponsibleParty_phone_voice': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
    'contact_CI_ResponsibleParty_address_deliveryPoint': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
    'contact_CI_ResponsibleParty_address_city': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
    'contact_CI_ResponsibleParty_address_postalCode': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'),
    'contact_CI_ResponsibleParty_address_country': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString'),
    'contact_CI_ResponsibleParty_email': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),
    'contact_CI_ResponsibleParty_role_CI_RoleCode': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode'),

    # Identification Information
    'identificationInfo_MD_DataIdentification_citation_title': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString'),
    'identificationInfo_MD_DataIdentification_citation_date': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'),
    'identificationInfo_MD_DataIdentification_citation_edition': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:edition/gco:CharacterString'),
    'identificationInfo_MD_DataIdentification_abstract': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString'),
    'identificationInfo_MD_DataIdentification_purpose': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose/gco:CharacterString'),
    'identificationInfo_MD_DataIdentification_status_MD_ProgressCode': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode'),
    'identificationInfo_MD_DataIdentification_descriptiveKeywords_place': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString'),
    'identificationInfo_MD_DataIdentification_descriptiveKeywords_theme': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:type/gmd:MD_KeywordTypeCode'),
    'identificationInfo_MD_DataIdentification_spatialRepresentationType': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode'),
    'identificationInfo_MD_DataIdentification_topicCategory': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode'),

    # Geographic Bounding Box
    'identificationInfo_MD_DataIdentification_extent_geographicBoundingBox_westBoundLongitude': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal'),
    'identificationInfo_MD_DataIdentification_extent_geographicBoundingBox_eastBoundLongitude': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal'),
    'identificationInfo_MD_DataIdentification_extent_geographicBoundingBox_southBoundLatitude': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal'),
    'identificationInfo_MD_DataIdentification_extent_geographicBoundingBox_northBoundLatitude': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal'),

    # Temporal Extent
    'identificationInfo_MD_DataIdentification_extent_temporalExtent_start': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition'),
    'identificationInfo_MD_DataIdentification_extent_temporalExtent_end': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition'),

    # Responsible Party for Dataset
    'citedResponsibleParty_CI_ResponsibleParty_individualName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
    'citedResponsibleParty_CI_ResponsibleParty_organisationName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
    'citedResponsibleParty_CI_ResponsibleParty_positionName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
    'citedResponsibleParty_CI_ResponsibleParty_contactInfo_phone_voice': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
    'citedResponsibleParty_CI_ResponsibleParty_contactInfo_phone_facsimile': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString'),
    'citedResponsibleParty_CI_ResponsibleParty_contactInfo_address_deliveryPoint': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
    'citedResponsibleParty_CI_ResponsibleParty_contactInfo_address_city': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
    'citedResponsibleParty_CI_ResponsibleParty_contactInfo_address_country': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString'),
    'citedResponsibleParty_CI_ResponsibleParty_contactInfo_address_email': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),

    # Point of Contact
    'pointOfContact_CI_ResponsibleParty_individualName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
    'pointOfContact_CI_ResponsibleParty_organisationName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
    'pointOfContact_CI_ResponsibleParty_positionName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
    'pointOfContact_CI_ResponsibleParty_contactInfo_phone_voice': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
    'pointOfContact_CI_ResponsibleParty_contactInfo_address_deliveryPoint': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
    'pointOfContact_CI_ResponsibleParty_contactInfo_address_city': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
    'pointOfContact_CI_ResponsibleParty_contactInfo_address_country': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString'),

    # Distributor Contact
    'distributorContact_CI_ResponsibleParty_individualName': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
    'distributorContact_CI_ResponsibleParty_organisationName': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
    'distributorContact_CI_ResponsibleParty_positionName': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
    'distributorContact_CI_ResponsibleParty_contactInfo_phone_voice': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
    'distributorContact_CI_ResponsibleParty_contactInfo_phone_facsimile': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString'),
    'distributorContact_CI_ResponsibleParty_contactInfo_address_deliveryPoint': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
    'distributorContact_CI_ResponsibleParty_contactInfo_address_city': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
    'distributorContact_CI_ResponsibleParty_contactInfo_address_country': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString'),
    'distributorContact_CI_ResponsibleParty_contactInfo_address_email': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),

    # Data Quality Information
    'dataQualityInfo_DQ_DataQuality_scope_level_MD_ScopeCode': get_text('./gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode'),
    'dataQualityInfo_DQ_DataQuality_lineage_statement': get_text('./gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString'),

    # Legal Constraints
    'metadataConstraints_MD_LegalConstraints_useLimitation': get_text('./gmd:metadataConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString'),
    'metadataConstraints_MD_LegalConstraints_useConstraints': get_text('./gmd:metadataConstraints/gmd:MD_LegalConstraints/gmd:useConstraints/gmd:MD_RestrictionCode'),
}


d2 = {
    # Additional Identification Information
    'identificationInfo_MD_DataIdentification_alternateTitle': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:alternateTitle/gco:CharacterString'),
    'identificationInfo_MD_DataIdentification_citation_otherCitationDetails': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:otherCitationDetails/gco:CharacterString'),
    'identificationInfo_MD_DataIdentification_citation_editionDate': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:editionDate/gco:Date'),

    # Temporal Information
    'identificationInfo_MD_DataIdentification_extent_temporalExtent_fullRange': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod'),

    # Spatial Resolution
    'identificationInfo_MD_DataIdentification_spatialResolution': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance'),

    # Reference System Information
    'referenceSystemInfo_MD_ReferenceSystem_referenceSystemIdentifier': get_text('./gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString'),

    # Constraints Information
    'metadataConstraints_MD_LegalConstraints_otherConstraints': get_text('./gmd:metadataConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString'),
    'metadataConstraints_MD_SecurityConstraints_classification': get_text('./gmd:metadataConstraints/gmd:MD_SecurityConstraints/gmd:classification/gmd:MD_ClassificationCode'),

    # Data Quality Information
    'dataQualityInfo_DQ_DataQuality_scope': get_text('./gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode'),

    # Maintenance Information
    'resourceMaintenance_MD_MaintenanceInformation_frequency': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode'),

    # Distribution Information
    'distributionInfo_MD_Distribution_distributionFormat': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString'),
    'distributionInfo_MD_Distribution_onlineResource': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'),

    # Lineage Information
    'dataQualityInfo_DQ_DataQuality_lineage_statement': get_text('./gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString'),

    # Additional Contact Roles
    'contact_CI_ResponsibleParty_originator': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
    'contact_CI_ResponsibleParty_publisher': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString')
}

merged_dict = d1 | d2 
# Sorting the merged dictionary by keys
ordered_dict = dict(sorted(merged_dict.items()))

print("Merged Dictionary:", merged_dict)
print("Ordered Dictionary:", ordered_dict)