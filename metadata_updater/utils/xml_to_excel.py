import os
import xml.etree.ElementTree as ET
import openpyxl

def parse_xml_file(file_path):
    """
    Extract the metadata from the metadata XML document
    """

    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'gco': 'http://www.isotc211.org/2005/gco',
        'srv': 'http://www.isotc211.org/2005/srv',
        'gml': 'http://www.opengis.net/gml',
        'xlink': 'http://www.w3.org/1999/xlink',
        'gts': 'http://www.isotc211.org/2005/gts'
    }

    def get_text(path):
        found = root.find(path, namespaces)
        return found.text if found is not None else ''

    data = {
        # Metadata information'
        'metadata_fileIdentifier': get_text('./gmd:fileIdentifier/gco:CharacterString'),
        'metadata_Language_LanguageCode': get_text('./gmd:language/gmd:LanguageCode'),
        'metadata_MD_CharacterSetCode_LanguageCode': get_text('./gmd:characterSet/gmd:MD_CharacterSetCode'),
        'metadata_hierarchyLevel_scope': get_text('./gmd:hierarchyLevel/gmd:MD_ScopeCode'),
        'metadata_hierarchyLevelName': get_text('./gmd:hierarchyLevelName/gco:CharacterString'),
        'dateStamp_Date': get_text('./gmd:dateStamp/gco:Date'),
        'metadataStandardName_CharacterString': get_text('./gmd:metadataStandardName/gco:CharacterString'),
        'metadataStandardVersion_CharacterString': get_text('./gmd:metadataStandardVersion/gco:CharacterString'),

        # Root - CI_ResponsibleParty
        'contact_CI_ResponsibleParty_individualName': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
        'contact_CI_ResponsibleParty_organisationName': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
        'contact_CI_ResponsibleParty_positionName': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
        'contact_CI_ResponsibleParty_contactInfo_phone_voice': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
        'contact_CI_ResponsibleParty_contactInfo_phone_facsimile': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString'),
        'contact_CI_ResponsibleParty_contactInfo_address_deliveryPoint': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
        'contact_CI_ResponsibleParty_contactInfo_address_city': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
        'contact_CI_ResponsibleParty_contactInfo_address_administrativeArea': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString'),
        'contact_CI_ResponsibleParty_contactInfo_address_postalCode': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'),
        'contact_CI_ResponsibleParty_contactInfo_address_country': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gmd:Country'),
        'contact_CI_ResponsibleParty_contactInfo_email': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),
        'contact_CI_ResponsibleParty_role': get_text('./gmd:contact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode'),


        # MD_DataIdentification 
        # MD_DataIdentification - Point of contact
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_individualName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_organisationName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_positionName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_contactInfo_CI_Contact_phone_CI_Telephone_voice': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_contactInfo_CI_Contact_phone_CI_Telephone_facsimile': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_deliveryPoint': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_city': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_administrativeArea': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_postalCode': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_country': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gmd:Country'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_electronicMailAddress': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_pointOfContact_CI_ResponsibleParty_role': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode'),

        # MD_DataIdentification - identificationInfo
        'identificationInfo_MD_DataIdentification_abstract': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_purpose': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_credit': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:credit/gco:CharacterString'),
        # MD_DataIdentification - Citation
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_title': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_alternateTitle': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:alternateTitle/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_date_CI_Date_date': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_date_CI_Date_dateType': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_edition': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:edition/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_editionDate': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:editionDate/gco:Date'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_identifier_MD_Identifier_authority_CI_Citation_title': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:authority/gmd:CI_Citation/gmd:title/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_identifier_MD_Identifier_authority_CI_Citation_date_CI_Date_date': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:authority/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_identifier_MD_Identifier_code': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString'),
        # MD_DataIdentification - Citation - CI_ResponsibleParty
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_individualName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_organisationName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_positionName': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_contactInfo_CI_Contact_phone_CI_Telephone_voice': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_contactInfo_CI_Contact_phone_CI_Telephone_facsimile': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_deliveryPoint': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_city': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_administrativeArea': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_postalCode': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_country': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gmd:Country'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_contactInfo_CI_Contact_address_CI_Address_electronicMailAddress': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),
        # Role
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_citedResponsibleParty_CI_ResponsibleParty_role': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode'),
        # other
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_presentationForm_CI_PresentationFormCode': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_otherCitationDetails': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:otherCitationDetails/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_citation_CI_Citation_collectiveTitle': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:collectiveTitle/gco:CharacterString'),

        # identificationInfo resourceMaintenance
        'identificationInfo_MD_DataIdentification_resourceMaintenance_MD_MaintenanceInformation_maintenanceAndUpdateFrequency_MD_MaintenanceFrequencyCode': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode'),
        'identificationInfo_MD_DataIdentification_resourceMaintenance_MD_MaintenanceInformation_userDefinedMaintenanceFrequency': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:userDefinedMaintenanceFrequency/gts:TM_PeriodDuration'),
        'identificationInfo_MD_DataIdentification_resourceMaintenance_MD_MaintenanceInformation_maintenanceNote': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceNote/gco:CharacterString'),

        # Distribution  information 
        'distributionInfo_MD_Distribution_distributionFormat_MD_Format_name': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString'),
        'distributionInfo_MD_Distribution_distributionFormat_MD_Format_version': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:version/gco:CharacterString'),
        'distributionInfo_MD_Distribution_transferOptions_MD_DigitalTransferOptions_unitsOfDistribution': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString'),
        'distributionInfo_MD_Distribution_transferOptions_MD_DigitalTransferOptions_transferSize': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:transferSize/gco:Real'),
        'distributionInfo_MD_Distribution_transferOptions_MD_DigitalTransferOptions_onLine_CI_OnlineResource_linkage': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'),

        # Distributor information 
        'distributorContact_CI_ResponsibleParty_individualName': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
        'distributorContact_CI_ResponsibleParty_organisationName': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
        'distributorContact_CI_ResponsibleParty_positionName': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
        'distributorContact_CI_ResponsibleParty_contactInfo_phone_voice': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
        'distributorContact_CI_ResponsibleParty_contactInfo_phone_facsimile': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString'),
        'distributorContact_CI_ResponsibleParty_contactInfo_address_deliveryPoint': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
        'distributorContact_CI_ResponsibleParty_contactInfo_address_city': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
        'distributorContact_CI_ResponsibleParty_contactInfo_address_administrativeArea': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/gco:CharacterString'),        
        'distributorContact_CI_ResponsibleParty_contactInfo_address_postalCode': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'),
        'distributorContact_CI_ResponsibleParty_contactInfo_address_country': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gmd:Country'),
        'distributorContact_CI_ResponsibleParty_contactInfo_address_email': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),
        'distributionContact_CI_ResponsibleParty_role': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:role'),

        # In reality there a multiple entries for the below 
        # Keywords
        'identificationInfo_MD_DataIdentification_descriptiveKeywords': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString'),

        # In reality there a multiple entries for the below 
        # topics
        'identificationInfo_MD_DataIdentification_topicCategory': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode'),


        # Constraints
        'identificationInfo_MD_DataIdentification_resourceConstraints_MD_LegalConstraints_accessConstraints_MD_RestrictionCode': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode'),
        'identificationInfo_MD_DataIdentification_resourceConstraints_MD_LegalConstraints_useConstraints_MD_RestrictionCode': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useConstraints/gmd:MD_RestrictionCode'),
        'identificationInfo_MD_DataIdentification_resourceConstraints_MD_LegalConstraints_otherConstraints': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString'),

        # Spatial Details
        'identificationInfo_MD_DataIdentification_spatialRepresentationType': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode'),
        'identificationInfo_MD_DataIdentification_spatialResolution_MD_Resolution_equivalentScale_MD_RepresentativeFraction_denominator': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer'),
        'identificationInfo_MD_DataIdentification_spatialResolution_MD_Resolution_distance': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance'),

        # other
        'identificationInfo_MD_DataIdentification_environmentDescription': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:environmentDescription/gco:CharacterString'),
        'identificationInfo_MD_DataIdentification_supplementalInformation': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/gco:CharacterString'),

        # Geographic Bounding Box
        'identificationInfo_MD_DataIdentification_extent_geographicBoundingBox_westBoundLongitude': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal'),
        'identificationInfo_MD_DataIdentification_extent_geographicBoundingBox_eastBoundLongitude': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal'),
        'identificationInfo_MD_DataIdentification_extent_geographicBoundingBox_southBoundLatitude': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal'),
        'identificationInfo_MD_DataIdentification_extent_geographicBoundingBox_northBoundLatitude': get_text('./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal'),

        'distributionInfo_MD_Distribution_distributor_distributionOrderProcess': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributionOrderProcess/gmd:MD_StandardOrderProcess/gmd:orderingInstructions/gco:CharacterString'),
        'distributionInfo_MD_Distribution_distributor_distributorFormat_name': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorFormat/gmd:MD_Format/gmd:name/gco:CharacterString'),
        'distributionInfo_MD_Distribution_distributor_distributorFormat_version': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorFormat/gmd:MD_Format/gmd:version/gco:CharacterString'),
        'distributionInfo_MD_Distribution_distributor_distributorTransferOptions_transferSize': get_text('./gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorTransferOptions/gmd:MD_DigitalTransferOptions/gmd:transferSize/gco:Real'),

   

        # Spatial Representation Info
        'spatialRepresentationInfo_MD_VectorSpatialRepresentation_topologyLevel': get_text('./gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:topologyLevel/gmd:MD_TopologyLevelCode'),
        'spatialRepresentationInfo_MD_VectorSpatialRepresentation_geometricObjectType': get_text('./gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:geometricObjects/gmd:MD_GeometricObjects/gmd:geometricObjectType/gmd:MD_GeometricObjectTypeCode'),
        'spatialRepresentationInfo_MD_VectorSpatialRepresentation_geometricObjects_geometricObjectCount': get_text('./gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:geometricObjects/gmd:MD_GeometricObjects/gmd:geometricObjectCount/gco:Integer'),

        # referenceSystemInfo
        'referenceSystemInfo_MD_ReferenceSystem_referenceSystemIdentifier_RS_Identifier_code': get_text('./gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString'),
        'referenceSystemInfo_MD_ReferenceSystem_referenceSystemIdentifier_RS_Identifier_codeSpace': get_text('./gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString'),
        'referenceSystemInfo_MD_ReferenceSystem_referenceSystemIdentifier_RS_Identifier_version': get_text('./gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version/gco:CharacterString'),     

        # Data Quality Information
        'dataQualityInfo_DQ_DataQuality_scope_level_MD_ScopeCode': get_text('./gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode'),
        'dataQualityInfo_DQ_DataQuality_lineage_statement': get_text('./gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString'),

        # Legal Constraints
        'metadataConstraints_MD_LegalConstraints_useLimitation': get_text('./gmd:metadataConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString'),



    }
    return data

def write_to_excel(data_list, output_file):
    """
    Write a metadata summary to an Excel workbook
    """

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    headers = list(data_list[0].keys()) if data_list else []
    sheet.append(headers)

    for data in data_list:
        row = [data.get(header, '') for header in headers]
        sheet.append(row)

    workbook.save(output_file)

def record_missing_metadata(data, missing_metadata_file):
    """
    Record information in a spreadsheet for any layers that have no metadata attached
    """
    headers = ["layer_id", "layer_title", "layer_url", "__license_type", "__license_url", "__is_public"]

    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(headers)

        for entry in data:
            row = [entry.get(header) for header in headers]
            sheet.append(row)
        
        workbook.save(missing_metadata_file)
    except Exception as e:
        print(f"Failed to write to Excel: {e}")
