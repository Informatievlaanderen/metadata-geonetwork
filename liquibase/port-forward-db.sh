# Variables
DBDEPLOYMENT=deployment/postgres-geonetwork
DBPORT=5432

# Push commands in the background, when the script exits, the commands will exit too
kubectl --cluster pre-md-cluster-aks --namespace dev port-forward $DBDEPLOYMENT 5433:$DBPORT & \
kubectl --cluster pre-md-cluster-aks --namespace bet port-forward $DBDEPLOYMENT 5434:$DBPORT & \
#kubectl --cluster prd-md-cluster-aks --namespace prd port-forward $DBDEPLOYMENT 5435:$DBPORT & \

# Wait till we're done
echo "Press CTRL-C to stop port forwarding and exit the script"
wait
