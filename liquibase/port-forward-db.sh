# get user input
usage="$(basename "$0") [-h] [-p]
--------------------------------------------------
Set up port forwards to the GeoNetwork databases in the cluster(s). The local ports are kept stable so they can reliably be used in database connections.

where:
    -h  show this help text
    -p  include prd forward"
while getopts 'hp' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    p) prd=true
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

shift $((OPTIND - 1))
# Variables
DBDEPLOYMENT=deployment/postgres-geonetwork
DBPORT=5432

# Push commands in the background, when the script exits, the commands will exit too
kubectl --cluster pre-md-cluster-aks --namespace dev port-forward $DBDEPLOYMENT 5433:$DBPORT & \
kubectl --cluster pre-md-cluster-aks --namespace bet port-forward $DBDEPLOYMENT 5434:$DBPORT & \
if [[ $prd == true ]]; then
  echo "WARNING: production is accessible!"
  kubectl --cluster prd-md-cluster-aks --namespace prd port-forward $DBDEPLOYMENT 5435:$DBPORT & \
fi

# Wait till we're done
echo "Press CTRL-C to stop port forwarding and exit the script"
wait
