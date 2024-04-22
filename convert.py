import xml.etree.ElementTree as ET

def convert_vissim_23(path_input, path_output) -> None:
    '''Downgrade from vissim 23 to vissim 10.'''
    tree = ET.parse(path_input)
    network = tree.getroot()

    network.attrib['version'] = '503'
    network.attrib['vissimVersion'] = '10.00 - 16 [79178]'


    for tag_backgroundImage in network.findall('./backgroundImages/backgroundImage'):
        if tag_backgroundImage.attrib['pathFilename'][:6] == '#data#':
            tag_backgroundImage.attrib['pathFilename'] = tag_backgroundImage.attrib['pathFilename'][6:]
            del tag_backgroundImage.attrib['type']
        tag_coordBL = tag_backgroundImage.find('./coordBL')
        tag_coordBL.tag = 'posBL'
        tag_coordTR = tag_backgroundImage.find('./coordTR')
        tag_coordTR.tag = 'posTR'

    for tag_conflictArea in network.findall('./conflictAreas/conflictArea'):
        del tag_conflictArea.attrib['conflTypDetmAuto']
        del tag_conflictArea.attrib['conflTypMan']

    for tag_displayTypes in network.findall('./displayTypes/displayType'):
        del tag_displayTypes.attrib['drawOrder3D']
    
    for tag_drivingBehavior in network.findall('./drivingBehaviors/drivingBehavior'):
        del tag_drivingBehavior.attrib['conflArAsInteractObj']
        del tag_drivingBehavior.attrib['distractProb']
        del tag_drivingBehavior.attrib['enforcAbsBrakDist']
        del tag_drivingBehavior.attrib['incrsAccel']
        tag_drivingBehavior.attrib.pop('jerkLimit', None)
        del tag_drivingBehavior.attrib['maxNumPlatoonVeh']
        del tag_drivingBehavior.attrib['maxPlatoonApprDist']
        del tag_drivingBehavior.attrib['maxPlatoonDesSpeed']
        tag_drivingBehavior.attrib['minHdwy'] = tag_drivingBehavior.attrib['minFrontRearClear']
        del tag_drivingBehavior.attrib['minFrontRearClear']
        tag_drivingBehavior.attrib['obsrvdVehs'] =tag_drivingBehavior.attrib['numInteractObj']
        del tag_drivingBehavior.attrib['numInteractObj']
        del tag_drivingBehavior.attrib['numInteractVeh']
        del tag_drivingBehavior.attrib['platoonFollowUpGapTm']
        del tag_drivingBehavior.attrib['platoonMinClear']
        del tag_drivingBehavior.attrib['platoonPoss']
        tag_drivingBehavior.attrib['smthClsup'] = "true"
        del tag_drivingBehavior.attrib['useImplicStoch']

        d = {k: tag_drivingBehavior.attrib[k] for k in sorted(tag_drivingBehavior.attrib)}
        tag_drivingBehavior.attrib.clear()
        tag_drivingBehavior.attrib.update(d)



    # <dynamicAssignment/>
    #tag_dynamicAssignment = network.find('./dynamicAssignment')
    #tag_matrixCorrectionParameters = tag_dynamicAssignment.find('./matrixCorrectionParameters')
    #tag_dynamicAssignment.remove(tag_matrixCorrectionParameters)

    # <evaluation/>
    tag_evaluation = network.find('./evaluation')
    tag_evaluation.attrib.pop('boschEmiCalcAct', None)
    tag_evaluation.attrib['queueMaxHeadway'] = tag_evaluation.attrib['queueMaxClear']
    del tag_evaluation.attrib['queueMaxClear']
    d = {k: tag_evaluation.attrib[k] for k in sorted(tag_evaluation.attrib)}
    tag_evaluation.attrib.clear()
    tag_evaluation.attrib.update(d)

    #tag_convergence = tag_evaluation.find('./convergence')
    #tag_evaluation.remove(tag_convergence)
    #tag_mesoEvaluationConfig = tag_evaluation.find('./mesoEvaluationConfig')
    #tag_evaluation.remove(tag_mesoEvaluationConfig)
    #tag_odPairs = tag_evaluation.find('./odPairs')
    #tag_evaluation.remove(tag_odPairs)
    tag_parkLotGrps = tag_evaluation.find('./parkLotGrps')
    tag_evaluation.remove(tag_parkLotGrps)
    tag_parkLots = tag_evaluation.find('./parkLots')
    tag_evaluation.remove(tag_parkLots)
    tag_parkRoutDecs=tag_evaluation.find('./parkRoutDecs')
    tag_evaluation.remove(tag_parkRoutDecs)
    tag_parkSpcs = tag_evaluation.find('./parkSpcs')
    tag_evaluation.remove(tag_parkSpcs)
    tag_ssam = tag_evaluation.find('./ssam')
    del tag_ssam.attrib['fromTime']
    del tag_ssam.attrib['toTime']
    tag_vehInps = tag_evaluation.find('./vehInps')
    tag_evaluation.remove(tag_vehInps)

    tag_laneMarkingTypes = network.find('laneMarkingTypes')
    if tag_laneMarkingTypes is not None:
        network.remove(tag_laneMarkingTypes)

    for tag_link in network.findall('./links/link'):
        del tag_link.attrib['consVehInDynPot']
        del tag_link.attrib['desSpeedFact']
        tag_link.attrib.pop('emiCalcAct', None)
        del tag_link.attrib['netPerfEvalAct']
        tag_link.attrib.pop('rvsPark', None)
        del tag_link.attrib['vehDynPotG']

        tag_linkPolyPts = tag_link.find('./geometry/linkPolyPts')
        tag_linkPolyPts.tag = 'points3D'

        for tag_linkPolyPoint in tag_linkPolyPts:
            tag_linkPolyPoint.tag = 'point3D'
            tag_linkPolyPoint.attrib.pop('radiusEffect', None)
            tag_linkPolyPoint.attrib.pop('radiusSrc', None)
            tag_linkPolyPoint.attrib.pop('rad', None)
            tag_linkPolyPoint.attrib.pop('radiusEffect', None)

        for tag_lane in tag_link.findall('./lanes/lane'):
            tag_lane.attrib.pop('markingType', None)

    for tag_model2D3DSegment in network.findall('./models2D3D/model2D3D/model2D3DSegs/model2D3DSegment'):
        tag_model2D3DSegment.attrib.pop('motionAnim', None)
        tag_model2D3DSegment.attrib.pop('partWOutPassFront', None)
        tag_model2D3DSegment.attrib.pop('partWOutPassRear', None)
        tag_model2D3DSegment.attrib['file3D'] = tag_model2D3DSegment.attrib['file3D'].replace('.fbx','.v3d')
        if tag_model2D3DSegment.attrib['file3D'][:6] == '#data#':
            tag_model2D3DSegment.attrib['file3D'] = tag_model2D3DSegment.attrib['file3D'][6:]

    tag_netPara = network.find('./netPara')
    tag_netPara.attrib['databFilename'] = ""
    tag_netPara.attrib.pop('speedLimCurves', None)
    del tag_netPara.attrib['underScenMngm']
    d = {k: tag_netPara.attrib[k] for k in sorted(tag_netPara.attrib)}
    tag_netPara.attrib.clear()
    tag_netPara.attrib.update(d)

    for tag_node in network.findall('./nodes/node'):
        tag_node.attrib.pop('allowRecr', None)
        tag_node.attrib.pop('mesoPenalMerg', None)

    tag_signalControllers = network.find('./signalControllers')
    if tag_signalControllers is not None:
        network.remove(tag_signalControllers)

    for tag_reducedSpedArea in network.findall('./reducedSpeedAreas/reducedSpeedArea'):
        tag_reducedSpedArea.attrib['timeTo'] = str(min(99999, int(tag_reducedSpedArea.attrib['timeTo'])))

    for tag_userDefinedAttribute in network.findall('./userDefinedAttributes/userDefinedAttribute'):
        del tag_userDefinedAttribute.attrib['canBeEmpty']

    for tag_vehicleType in network.findall('./vehicleTypes/vehicleType'):
        tag_vehicleType.attrib['clearTm'] = tag_vehicleType.attrib['clearTmPT']
        del tag_vehicleType.attrib['clearTmPT']

        d = {k: tag_vehicleType.attrib[k] for k in sorted(tag_vehicleType.attrib)}
        tag_vehicleType.attrib.clear()
        tag_vehicleType.attrib.update(d)

    for tag_vehicleRoutingDecisionStatic in network.findall('./vehicleRoutingDecisionsStatic/vehicleRoutingDecisionStatic'):
        del tag_vehicleRoutingDecisionStatic.attrib['routeChoiceMeth']
        for tag_vehileRouteStatic in tag_vehicleRoutingDecisionStatic.findall('./vehRoutSta/vehicleRouteStatic'):
            del tag_vehileRouteStatic.attrib['formula']

    tree.write(path_output, encoding='utf-8', xml_declaration=True)

def convert_vissim_24(path_input, path_output) -> None:
    """ Downgrade from Vissim.24 to Vissim.100 """

    tree = ET.parse(path_input)
    network = tree.getroot()

    network.attrib['version'] = '503'
    network.attrib['vissimVersion'] = '10.00 - 16 [79178]'

    try:
        for tag_backgroundImage in network.findall('./backgroundImages/backgroundImage'):
            if tag_backgroundImage.attrib['pathFilename'][:6] == '#data#':
                tag_backgroundImage.attrib['pathFilename'] = tag_backgroundImage.attrib['pathFilename'][6:]
                del tag_backgroundImage.attrib['type']
            if '.-' in tag_backgroundImage.attrib['pathFilename']:
                tag_backgroundImage.attrib['pathFilename'] = tag_backgroundImage.attrib['pathFilename'].replace('.-', '.')
            tag_coordBL = tag_backgroundImage.find('./coordBL')
            tag_coordBL.tag = 'posBL'
            tag_coordTR = tag_backgroundImage.find('./coordTR')
            tag_coordTR.tag = 'posTR'
    except: pass

    try:
        for tag_conflictArea in network.findall('./conflictAreas/conflictArea'):
            linkA_value = tag_conflictArea.get('linkA')
            tag_conflictArea.set("link1",linkA_value)
            tag_conflictArea.attrib.pop('linkA', None)

            linkB_value = tag_conflictArea.get('linkB')
            tag_conflictArea.set("link2",linkB_value)
            tag_conflictArea.attrib.pop('linkB', None)

            visibLinkA = tag_conflictArea.get('visibLinkA')
            tag_conflictArea.set("visibLink1",visibLinkA)
            tag_conflictArea.attrib.pop('visibLinkA', None)

            visibLinkB = tag_conflictArea.get('visibLinkB')
            tag_conflictArea.set("visibLink2",visibLinkB)
            tag_conflictArea.attrib.pop('visibLinkB', None)

            del tag_conflictArea.attrib['conflTypDetmAuto']
            del tag_conflictArea.attrib['conflTypMan']
    except: pass

    for tag_displayTypes in network.findall('./displayTypes/displayType'):
        del tag_displayTypes.attrib['drawOrder3D']

    try:
        for tag_drivingBehavior in network.findall('./drivingBehaviors/drivingBehavior'):
            tag_drivingBehavior.attrib['advMerg'] = "true"
            del tag_drivingBehavior.attrib['conflArAsInteractObj']
            del tag_drivingBehavior.attrib['distractProb']
            del tag_drivingBehavior.attrib['enforcAbsBrakDist']
            del tag_drivingBehavior.attrib['incrsAccel']
            tag_drivingBehavior.attrib.pop('jerkLimit',None)
            del tag_drivingBehavior.attrib['maxNumPlatoonVeh']
            del tag_drivingBehavior.attrib['maxPlatoonApprDist']
            del tag_drivingBehavior.attrib['maxPlatoonDesSpeed']
            tag_drivingBehavior.attrib['minHdwy'] = tag_drivingBehavior.attrib['minFrontRearClear']
            del tag_drivingBehavior.attrib['minFrontRearClear']
            tag_drivingBehavior.attrib['obsrvdVehs'] =tag_drivingBehavior.attrib['numInteractObj']
            del tag_drivingBehavior.attrib['numInteractObj']
            del tag_drivingBehavior.attrib['numInteractVeh']
            del tag_drivingBehavior.attrib['platoonFollowUpGapTm']
            del tag_drivingBehavior.attrib['platoonMinClear']
            del tag_drivingBehavior.attrib['platoonPoss']
            tag_drivingBehavior.attrib['smthClsup'] = "true"
            del tag_drivingBehavior.attrib['useImplicStoch']
            del tag_drivingBehavior.attrib['zipper']
            del tag_drivingBehavior.attrib['zipperMinSpeed']

            d = {k: tag_drivingBehavior.attrib[k] for k in sorted(tag_drivingBehavior.attrib)}
            tag_drivingBehavior.attrib.clear()
            tag_drivingBehavior.attrib.update(d)
    except: pass

    try:
        tag_evaluation = network.find('./evaluation')
        tag_evaluation.attrib.pop('boschEmiCalcAct', None)
        tag_evaluation.attrib['queueMaxHeadway'] = tag_evaluation.attrib['queueMaxClear']
        del tag_evaluation.attrib['queueMaxClear']
        d = {k: tag_evaluation.attrib[k] for k in sorted(tag_evaluation.attrib)}
        tag_evaluation.attrib.clear()
        tag_evaluation.attrib.update(d)
        tag_parkLotGrps = tag_evaluation.find('./parkLotGrps')
        tag_evaluation.remove(tag_parkLotGrps)
        tag_parkLots = tag_evaluation.find('./parkLots')
        tag_evaluation.remove(tag_parkLots)
        tag_parkRoutDecs = tag_evaluation.find('./parkRoutDecs')
        tag_evaluation.remove(tag_parkRoutDecs)
        tag_parkSpcs = tag_evaluation.find('./parkSpcs')
        tag_evaluation.remove(tag_parkSpcs)
        tag_ssam = tag_evaluation.find('./ssam')
        del tag_ssam.attrib['fromTime']
        del tag_ssam.attrib['toTime']
        tag_vehInps = tag_evaluation.find('./vehInps')
        tag_evaluation.remove(tag_vehInps)
    except: pass

    try:
        tag_laneMarkingTypes = network.find('./laneMarkingTypes')
        if tag_laneMarkingTypes is not None:
            network.remove(tag_laneMarkingTypes)
    except: pass

    try:
        for tag_link in network.find('./links/link'):
            del tag_link.attrib['consVehInDynPot']
            del tag_link.attrib['desSpeedFact']
            tag_link.attrib.pop('emiCalcAct', None)
            del tag_link.attrib['netPerfEvalAct']
            tag_link.attrib.pop('rvsPark', None)
            del tag_link.attrib['vehDynPotG']

            tag_linkPolyPts = tag_link.find('./geometry/linkPolyPts')
            tag_linkPolyPts.tag = 'points3D'

            for tag_linkPolyPoint in tag_linkPolyPts:
                tag_linkPolyPoint.tag = 'point3D'
                tag_linkPolyPoint.attrib.pop('radiusEffect', None)
                tag_linkPolyPoint.attrib.pop('radiusSrc', None)
                tag_linkPolyPoint.attrib.pop('rad', None)
                tag_linkPolyPoint.attrib.pop('radiusEffect', None)

            for tag_lane in tag_link.findall('./lanes/lane'):
                tag_lane.attrib.pop('markingType', None)
    except: pass

    try:
        for tag_model2D3DSegment in network.findall('./models2D3D/model2D3D/model2D3DSegs/model2D3DSegment'):
            tag_model2D3DSegment.attrib.pop('motionAnim', None)
            tag_model2D3DSegment.attrib.pop('partWOutPassFront', None)
            tag_model2D3DSegment.attrib.pop('partWOutPassRear', None)
            tag_model2D3DSegment.attrib['file3D'] = tag_model2D3DSegment.attrib['file3D'].replace('.fbx','.v3d')
            if tag_model2D3DSegment.attrib['file3D'][:6] == '#data#':
                tag_model2D3DSegment.attrib['file3D'] = tag_model2D3DSegment.attrib['file3D'][6:]
    except: pass

    try:
        tag_netPara = network.find('./netPara')
        tag_netPara.attrib['databFilename'] = ""
        tag_netPara.attrib.pop('speedLimCurves', None)
        del tag_netPara.attrib['underScenMngm']
        d = {k: tag_netPara.attrib[k] for k in sorted(tag_netPara.attrib)}
        tag_netPara.attrib.clear()
        tag_netPara.attrib.update(d)
    except: pass

    try:
        for tag_node in network.findall('./nodes/node'):
            tag_node.attrib.pop('allowRecr', None)
            tag_node.attrib.pop('mesoPenalMerg', None)
    except: pass

    try:
        tag_parkingLots = network.find('parkingLots')
        if tag_parkingLots is not None:
            network.remove(tag_parkingLots)
    except: pass

    try:
        for tag_pavementMarking in network.findall('./pavementMarkings/pavementMarking'):
            tag_pavementMarking.attrib.pop('texFile', None)
            tag_pavementMarking.attrib.pop('width', None)
    except: pass

    try:
        for tag_reducedSpeedArea in network.findall('./reducedSpeedAreas/reducedSpeedArea'):
            tag_reducedSpeedArea.attrib['timeTo'] = str(min(99999, int(tag_reducedSpeedArea.attrib['timeTo']))) 
    except:
        pass

    try:
        tag_signalControllers = network.find('./signalControllers')
        if tag_signalControllers is not None:
            network.remove(tag_signalControllers)
    except: pass

    try:
        tag_signalHeads = network.find('./signalHeads')
        if tag_signalHeads is not None:
            network.remove(tag_signalHeads)
    except: pass

    try:
        for tag_userDefinedAttribute in network.findall('./userDefinedAttributes/userDefinedAttribute'):
            del tag_userDefinedAttribute.attrib['canBeEmpty']
    except: pass

    #Falta analizar los vehicleRoutingDecisionsParking en el V10

    try:
        for tag_vehicleRoutingDecisionStatic in network.findall('./vehicleRoutingDecisionsStatic/vehicleRoutingDecisionStatic'):
            del tag_vehicleRoutingDecisionStatic.attrib['routeChoiceMeth']
            for tag_vehicleRouteStatic in tag_vehicleRoutingDecisionStatic.findall('./vehRoutSta/vehicleRouteStatic'):
                del tag_vehicleRouteStatic.attrib['formula']
    except: pass

    try:
        for tag_vehicleType in network.findall('./vehicleTypes/vehicleType'):
            tag_vehicleType.attrib['clearTm'] = tag_vehicleType.attrib['clearTmPt']
            del tag_vehicleType.attrib['clearTmPt']

            d = {k: tag_vehicleType.attrib[k] for k in sorted(tag_vehicleType.attrib)}
            tag_vehicleType.attrib.clear()
            tag_vehicleType.attrib.update(d)
    except: pass

    tree.write(path_output, encoding='utf-8', xml_declaration=True)
