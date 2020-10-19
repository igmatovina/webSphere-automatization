#!/bin/bash

. was_user_pass
. config/was.properties



createUsers()
{
	wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_users.py"
	$wsadmin_exec
}	

test()
{
	wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f test.py"
	$wsadmin_exec
}	


createJDBCProviders()
{
wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_jdbc.py"
	$wsadmin_exec
}		




createQCF()
{
wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_qcf.py"
	$wsadmin_exec
}	


createQueues()
{
wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_queues.py"
	$wsadmin_exec
}	



createSharedLibraries()
{
wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_shared_libraries.py"
	$wsadmin_exec
}	



setEnvironmentVariables()
{
	wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_variable.py"
	$wsadmin_exec
}	




createActivationSpecification()
{
	wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_active_spec.py"
	$wsadmin_exec
}	


createDatasources()
{
wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						  -f configure_datasource.py"
	$wsadmin_exec
}	


securitySetup()
{

	wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
							-f configure_security_ldap.py"
	$wsadmin_exec
}	



setJvmProperties()
{
	wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_jvm.py"
	$wsadmin_exec
}	



importCertificate()
{
	wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						  -f configure_import_certificate.py"
	$wsadmin_exec
}	



configureGlobalDeployment()
{
    wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						-f configure_global_deploy.py"
	$wsadmin_exec

}	



configureClusters()
{
	wsadmin_exec="$PROFILE/bin/wsadmin.sh -username deploy -password $WAS_PASSWORD \
						  -f configure_servers_and_cluster.py"
	$wsadmin_exec

}




echo " Izaberite opciju "
echo "1 configureClusters"
echo "2 setJvmProperties"
echo "3 securitySetup"
echo "4 configureGlobalDeployment "
echo "5 setEnvironmentVariables"
echo "6 createUsers" 
echo "7 createSharedLibraries" 
echo "8 createJDBCProviders" 		
echo "9 createDatasources" 
echo "10 createQCF" 
echo "11 createQueues" 
echo "12 createActivationSpecification" 
echo "13 importCertificate"  
echo "14 EXECUTE ALL"
echo "15 EXIT" 


read num

case $num in 

1) configureClusters;;
2) setJvmProperties;;
3) securitySetup;;
4) configureGlobalDeployment;;
5) setEnvironmentVariables;;
6) createUsers;;
7) createSharedLibraries;;
8) createJDBCProviders;;
9) createDatasources;;
10) createQCF;;
11) createQueues;;
12) createActivationSpecification;;
13) importCertificate;;
20) test;;
14) configureClusters
	setJvmProperties
	securitySetup
	configureGlobalDeployment
    setEnvironmentVariables
    createUsers
    createSharedLibraries
    createJDBCProviders
    createDatasources		
    createQCF
	createQueues
	createActivationSpecification
	importCertificate;;
*) echo "bye";;

esac



#Restart WAS-a










