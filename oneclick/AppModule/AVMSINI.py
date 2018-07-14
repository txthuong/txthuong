import ConfigParser

class AVMSCFG():
    packageInitial = ''
    packageREV = ''
    packageRES = ''
    
    def __init__(self,cfgFile = r"C:\SVN\Configuration\IDS\AVMS_HL7.ini"):
        My_AvmsCfg = ConfigParser.ConfigParser()
        My_AvmsCfg.read(cfgFile)
        self.packageInitial = My_AvmsCfg.get('Package','AVMS_FW_Initial').strip()
        self.packageREV = My_AvmsCfg.get('Package','AVMS_FW_Reverse').strip()
        self.packageRES = My_AvmsCfg.get('Package','AVMS_FW_CausesReboot').strip()
        self.packageCOR = My_AvmsCfg.get('Package','IDS_FW_Corrupted').strip()
        self.packageNoRev = My_AvmsCfg.get('Package','AVMS_FW_NoReverse').strip()
        
        self.AVMS_Upgrade_Package_Revision = My_AvmsCfg.get('Package','AVMS_Upgrade_Package_Revision').strip()
        self.AVMS_Upgrade_Package_Name = My_AvmsCfg.get('Package','AVMS_Upgrade_Package_Name').strip()
        self.AVMS_Normal_Package_Revision = My_AvmsCfg.get('Package','AVMS_Normal_Package_Revision').strip()
        self.AVMS_Normal_Package_Name = My_AvmsCfg.get('Package','AVMS_Normal_Package_Name').strip()
        self.Model = My_AvmsCfg.get('Gateway','Model').strip()
        self.AVMS_SW_Upgrade_Package_Name = My_AvmsCfg.get('Package','AVMS_SW_Upgrade_Package').strip()
        self.AVMS_SW_Upgrade_Big_Package_Name = My_AvmsCfg.get('Package','AVMS_SW_Upgrade_Big_Package').strip()
        self.AVMS_SW_Revision_Initial = My_AvmsCfg.get('Package','AVMS_SW_Revision_Initial').strip()
        self.AVMS_SW_Revision_Target = My_AvmsCfg.get('Package','AVMS_SW_Revision_Target').strip()
        self.AVMS_SW_Type = My_AvmsCfg.get('Package','AVMS_SW_Type').strip()
        
        self.System_Name = My_AvmsCfg.get('Systems','System_Name').strip()
        self.System_uidFw = My_AvmsCfg.get('Systems','System_uidFw').strip()
        self.System_SN = My_AvmsCfg.get('Systems','System_SN').strip()
        self.System_Subscription_uid = My_AvmsCfg.get('Systems','System_Subscription_uid').strip()
        

if __name__ == '__main__':
    myAvmsCfg = AVMSCFG()
    print myAvmsCfg.packageNoRev
    print myAvmsCfg.packageInitial
