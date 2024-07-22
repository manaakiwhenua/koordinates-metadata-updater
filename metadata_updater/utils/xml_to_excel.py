import os
import xml.etree.ElementTree as ET
import openpyxl

def parse_xml_file(file_path):
    """
    Extract the metadata from the metadata xml document
    """

    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'gco': 'http://www.isotc211.org/2005/gco',
        'srv': 'http://www.isotc211.org/2005/srv',
        'gml': 'http://www.opengis.net/gml',
        'xlink': 'http://www.w3.org/1999/xlink'
    }

    def get_text(element, path):
        found = root.find(path, namespaces)
        return found.text if found is not None else ''

    data = {
        'language': get_text(root, './/gmd:language/gmd:LanguageCode'),
        'hierarchyLevel': get_text(root, './/gmd:hierarchyLevel/gmd:MD_ScopeCode'),
        'hierarchyLevelName': get_text(root, './/gmd:hierarchyLevelName/gco:CharacterString'),
        'individualName': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString'),
        'organisationName': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'),
        'positionName': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString'),
        'phone': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'),
        'email': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),
        'address': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
        'city': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'),
        'postalCode': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'),
        'country': get_text(root, './/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gmd:Country'),
        'abstract': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString'),
        'title': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString'),
        'purpose': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose/gco:CharacterString'),
        'credit': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:credit/gco:CharacterString'),
        'status': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode'),
        'dateStamp': get_text(root, './/gmd:dateStamp/gco:Date'),
        'metadataStandardName': get_text(root, './/gmd:metadataStandardName/gco:CharacterString'),
        'metadataStandardVersion': get_text(root, './/gmd:metadataStandardVersion/gco:CharacterString'),
        'environmentDescription': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:environmentDescription/gco:CharacterString'),
        'topologyLevel': get_text(root, './/gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:topologyLevel/gmd:MD_TopologyLevelCode'),
        'geometricObjectType': get_text(root, './/gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:geometricObjects/gmd:MD_GeometricObjects/gmd:geometricObjectType/gmd:MD_GeometricObjectTypeCode'),
        'geometricObjectCount': get_text(root, './/gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:geometricObjects/gmd:MD_GeometricObjects/gmd:geometricObjectCount/gco:Integer'),
        'referenceSystemCode': get_text(root, './/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString'),
        'referenceSystemCodeSpace': get_text(root, './/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString'),
        'referenceSystemVersion': get_text(root, './/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version/gco:CharacterString'),
        'keyword': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString'),
        'useLimitation': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation/gco:CharacterString'),
        'spatialRepresentationType': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode'),
        'distance': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance'),
        'characterSet': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet/gmd:MD_CharacterSetCode'),
        'topicCategory': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode'),
        'extentTypeCode': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:extentTypeCode/gco:Boolean'),
        'westBoundLongitude': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal'),
        'eastBoundLongitude': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal'),
        'southBoundLatitude': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal'),
        'northBoundLatitude': get_text(root, './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal'),
        'distributionFormatName': get_text(root, './/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString'),
        'distributionFormatVersion': get_text(root, './/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:version/gco:CharacterString'),
        'transferSize': get_text(root, './/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:transferSize/gco:Real'),
        'lineageStatement': get_text(root, './/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString')
    }

    return data

def write_to_excel(data_list, output_file):
    """
    Write a metadata summary to an excel Workbook
    """

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    headers = [
        '__layer_id' , 'Language', 'Hierarchy Level', 'Hierarchy Level Name', 'Individual Name', 'Organisation Name',
        'Position Name', 'Phone', 'Email', 'Address', 'City', 'Postal Code', 'Country', 'Abstract',
        'Title', 'Purpose', 'Credit', 'Status', 'Date Stamp', 'Metadata Standard Name',
        'Metadata Standard Version', 'Environment Description', 'Topology Level', 'Geometric Object Type',
        'Geometric Object Count', 'Reference System Code', 'Reference System Code Space', 'Reference System Version',
        'Keyword', 'Use Limitation', 'Spatial Representation Type', 'Distance', 'Character Set',
        'Topic Category', 'Extent Type Code', 'West Bound Longitude', 'East Bound Longitude', 'South Bound Latitude',
        'North Bound Latitude', 'Distribution Format Name', 'Distribution Format Version', 'Transfer Size', 
        'Lineage Statement', '__license_type', '__license_url', '__num_downloads', '__first_published_at', '__is_public'
    ]



    sheet.append(headers)

    for data in data_list:
        row = [
            data['__layer_id'],
            data['language'],
            data['hierarchyLevel'],
            data['hierarchyLevelName'],
            data['individualName'],
            data['organisationName'],
            data['positionName'],
            data['phone'],
            data['email'],
            data['address'],
            data['city'],
            data['postalCode'],
            data['country'],
            data['abstract'],
            data['title'],
            data['purpose'],
            data['credit'],
            data['status'],
            data['dateStamp'],
            data['metadataStandardName'],
            data['metadataStandardVersion'],
            data['environmentDescription'],
            data['topologyLevel'],
            data['geometricObjectType'],
            data['geometricObjectCount'],
            data['referenceSystemCode'],
            data['referenceSystemCodeSpace'],
            data['referenceSystemVersion'],
            data['keyword'],
            data['useLimitation'],
            data['spatialRepresentationType'],
            data['distance'],
            data['characterSet'],
            data['topicCategory'],
            data['extentTypeCode'],
            data['westBoundLongitude'],
            data['eastBoundLongitude'],
            data['southBoundLatitude'],
            data['northBoundLatitude'],
            data['distributionFormatName'],
            data['distributionFormatVersion'],
            data['transferSize'],
            data['lineageStatement'],
            data['__license_type'],
            data['__license_url'],
            data['__num_downloads'] ,
            data['__first_published_at'],
            str(data['__is_public'])
        ]
        sheet.append(row)

    workbook.save(output_file)


def record_missing_metadata(data, missing_metadata_file):
    """
    Record information in a spread sheet for any layers found
    that have not metadata attached
    """
    headers = ["layer_id", "layer_title", "layer_url", "__license_type", "__license_url", "__is_public"]

    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(headers)  # Add header

        for entry in data:
            row = [entry.get(header) for header in headers]
            sheet.append(row)
        
        workbook.save(missing_metadata_file)
    except Exception as e:
        print(f"Failed to write to Excel: {e}")