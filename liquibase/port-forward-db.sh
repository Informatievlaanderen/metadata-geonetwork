# Variables
DBDEPLOYMENT=deployment/postgres-geonetwork
DBPORT=5432

# Push commands in the background, when the script exits, the commands will exit too
kubectl --namespace "dev" port-forward $DBDEPLOYMENT 5433:$DBPORT & \
kubectl --namespace "bet" port-forward $DBDEPLOYMENT 5434:$DBPORT & \

# Wait till we're done
echo "Press CTRL-C to stop port forwarding and exit the script"
wait