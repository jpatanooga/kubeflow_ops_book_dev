MODEL_NAME=sklearn-iris-svm-s3
INPUT_PATH=@./iris-input.json
CLUSTER_IP=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
SERVICE_HOSTNAME=$(kubectl get inferenceservice sklearn-iris-svm-s3 -o jsonpath='{.status.url}' | cut -d "/" -f 3)
#curl -v -H "Host: ${SERVICE_HOSTNAME}" http://$CLUSTER_IP/v1/models/$MODEL_NAME:predict -d $INPUT_PATH

echo "Host: ${SERVICE_HOSTNAME}" http://$CLUSTER_IP/v1/models/$MODEL_NAME:predict -d $INPUT_PATH