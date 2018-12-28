#config here
#number of Peer
peer = ["192.168.100.11","192.168.100.12","192.168.100.13"]
#virtual ip
rip = ["192.168.100.51","192.168.100.52","192.168.100.53","192.168.100.54","192.168.100.55"]
gateway = "192.168.100.1"
#lv range 2-4
lv = 4
#finish

'''create_vi = 7
peer = ["192.168.100.11","192.168.100.12","192.168.100.13","192.168.100.14"]
rip = ["192.168.100.51","192.168.100.52","192.168.100.53","192.168.100.54","192.168.100.55","192.168.100.56","192.168.100.57"]
gateway = "192.168.100.1"
lv = 3'''

ripind = 0
x = 0
listloop = 0
listlv = []
while listloop in range(0,lv):
        listlv.append(listloop)
        listloop += 1
if lv < 2 or lv > 4:
	print("error: lv out of range \n#lv range 2-4")
else:
 towrite = ("! Configuration File for keepalived\n\n"
 "global_defs {\n"
 "   notification_email {\n"
 "     acassen@firewall.loc\n"
 "     failover@firewall.loc\n"
 "     sysadmin@firewall.loc\n"
 "   }\n"
 "   notification_email_from Alexandre.Cassen@firewall.loc\n"
 "   smtp_server 192.168.200.1\n"
 "   smtp_connect_timeout 30\n"
 "   router_id LVS_DEVEL\n"
 "   vrrp_skip_check_adv_addr\n"
 "#   vrrp_strict\n"
 "   vrrp_garp_interval 0\n"
 "   vrrp_gna_interval 0\n"
 "}\n\n")

 with open("testgen.conf", "w") as f:
	f.writelines(towrite)
	while ripind in range(ripind,len(rip)):
		metric = ripind+1001
		if ripind > 0:
                	listlv.insert(0,listlv[len(listlv)-1])
                	del listlv[len(listlv)-1]
		
		towrite1 = ("vrrp_instance VI_"+str(ripind+1)+" {\n"
		"\tstate Backup\n"
		"\tinterface ens37\n"
		"\tvirtual_router_id "+str(ripind+1)+"\n"
		"{% if hostvars[inventory_hostname].ansible_ens33.ipv4.address | ipaddr('int') % "+str(lv)+" == "+str(listlv[0])+" %}\n"
		"\tpriority 100\n"
		"{% elif hostvars[inventory_hostname].ansible_ens33.ipv4.address | ipaddr('int') % "+str(lv)+" == "+str(listlv[1])+" %}\n"
		"\tpriority 80\n")

		towrite3 = ("{% end if %}\n"
		"\tuse_vmac vrrp"+str(ripind+1)+"\n"
		"\t\tvmac_xmit_base\n"
		"\tadvert_int 1\n"
		"\tauthentication {\n"
		"\tauth_type PASS\n"
		"\tauth_pass 1111\n"
		"\t}\n"
		"\tvirtual_ipaddress {\n"
		"\t\t"+rip[ripind]+"/24\n"
		"\t}\n"
		"\tvirtual_routes {\n"
		"\t\t0.0.0.0/0 via "+gateway+" metric "+str(metric)+"\n"
		"\tunicast_peer {\n")
		
		towrite5 = ("\t}\n"
		"}\n\n")

		f.writelines(towrite1)
		if lv == 3:
			towrite2_1 = ("{% elif hostvars[inventory_hostname].ansible_ens33.ipv4.address | ipaddr('int') % "+str(lv)+" == "
			+str(listlv[2])+" %}\n"
                	"\tpriority 60\n")
			f.writelines(towrite2_1)

		if lv == 4:
			towrite2_2 = ("{% elif hostvars[inventory_hostname].ansible_ens33.ipv4.address | ipaddr('int') % "+str(lv)+" == "
                        +str(listlv[2])+" %}\n"
                        "\tpriority 60\n"
			"{% elif hostvars[inventory_hostname].ansible_ens33.ipv4.address | ipaddr('int') % "+str(lv)+
			" == "+str(listlv[3])+
                	" %}\n"
			"\tpriority 40\n")
			f.writelines(towrite2_2)
		f.writelines(towrite3)
		while x in range(0, len(peer)):
			towrite4 = ("\t\t"+peer[x]+"/24\n")
			f.writelines(towrite4)
			x = x+1
		f.writelines(towrite5)
		ripind += 1
		if x == len(peer):
			x = 0

 exit()
