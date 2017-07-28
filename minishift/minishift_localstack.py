import shutit 
import minishift

def setup():
	s1 = minishift.startup()
	s1.send('oc delete namespace localstack || true && sleep 10')
	s1.send('oc create namespace localstack')
	s1.send('oc project localstack')
	s1.send_file('/tmp/new_scc.yaml','''allowHostDirVolumePlugin: false
allowHostIPC: false
allowHostNetwork: false
allowHostPID: false
allowHostPorts: false
allowPrivilegedContainer: false
allowedCapabilities: null
apiVersion: v1
defaultAddCapabilities: null
fsGroup:
  type: MustRunAs
groups:
- system:authenticated
kind: SecurityContextConstraints
metadata:
  annotations:
    kubernetes.io/description: restricted denies access to all host features and requires
      pods to be run with a UID, and SELinux context that are allocated to the namespace.  This
      is the most restrictive SCC.
  name: restricted
  selfLink: /api/v1/securitycontextconstraintsrestricted
priority: null
readOnlyRootFilesystem: false
requiredDropCapabilities:
- KILL
- MKNOD
- SYS_CHROOT
runAsUser:
  type: RunAsAny
seLinuxContext:
  type: MustRunAs
supplementalGroups:
  type: RunAsAny
volumes:
- configMap
- downwardAPI
- emptyDir
- persistentVolumeClaim
- secret''')
	s1.send('oc update -f /tmp/new_scc.yaml')
	s1.send('''oc new-app -e DEBUG=1 localstack/localstack --name="localstack"''')
	host = s1.send_and_get_output(r"""minishift console --machine-readable | grep HOST | sed 's/^HOST=\(.*\)/\1/'""")
	s1.send_file('/tmp/routes.yaml','''apiVersion: v1
items:
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: apigateway
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/apigateway
  spec:
    host: apigateway-test.''' + host + '''.nip.io
    port:
      targetPort: 4567-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:44:17Z
        status: "True"
        type: Admitted
      host: apigateway-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: cloudformation
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/cloudformation
  spec:
    host: cloudformation-test.''' + host + '''.nip.io
    port:
      targetPort: 4581-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:48:45Z
        status: "True"
        type: Admitted
      host: cloudformation-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: cloudwatch
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/cloudwatch
  spec:
    host: cloudwatch-test.''' + host + '''.nip.io
    port:
      targetPort: 4582-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:45:18Z
        status: "True"
        type: Admitted
      host: cloudwatch-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: dynamodb
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/dynamodb
  spec:
    host: dynamodb-test.''' + host + '''.nip.io
    port:
      targetPort: 4569-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:48:58Z
        status: "True"
        type: Admitted
      host: dynamodb-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: dynamodbstreams
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/dynamodbstreams
  spec:
    host: dynamodbstreams-test.''' + host + '''.nip.io
    port:
      targetPort: 4570-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:50:06Z
        status: "True"
        type: Admitted
      host: dynamodbstreams-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: es
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/es
  spec:
    host: es-test.''' + host + '''.nip.io
    port:
      targetPort: 4578-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:50:52Z
        status: "True"
        type: Admitted
      host: es-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: firehose
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/firehose
  spec:
    host: firehose-test.''' + host + '''.nip.io
    port:
      targetPort: 4573-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:50:23Z
        status: "True"
        type: Admitted
      host: firehose-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: kinesis
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/kinesis
  spec:
    host: kinesis-test.''' + host + '''.nip.io
    port:
      targetPort: 4568-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:46:36Z
        status: "True"
        type: Admitted
      host: kinesis-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: lambda
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/lambda
  spec:
    host: lambda-test.''' + host + '''.nip.io
    port:
      targetPort: 4574-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:51:06Z
        status: "True"
        type: Admitted
      host: lambda-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: redshift
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/redshift
  spec:
    host: redshift-test.''' + host + '''.nip.io
    port:
      targetPort: 4577-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:46:59Z
        status: "True"
        type: Admitted
      host: redshift-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: route53
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/route53
  spec:
    host: route53-test.''' + host + '''.nip.io
    port:
      targetPort: 4580-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:50:37Z
        status: "True"
        type: Admitted
      host: route53-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: s3
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/s3
  spec:
    host: s3-test.''' + host + '''.nip.io
    port:
      targetPort: 4572-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:48:14Z
        status: "True"
        type: Admitted
      host: s3-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: ses
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/ses
  spec:
    host: ses-test.''' + host + '''.nip.io
    port:
      targetPort: 4579-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:46:15Z
        status: "True"
        type: Admitted
      host: ses-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: sns
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/sns
  spec:
    host: sns-test.''' + host + '''.nip.io
    port:
      targetPort: 4575-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:49:42Z
        status: "True"
        type: Admitted
      host: sns-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      openshift.io/host.generated: "true"
    name: sqs
    namespace: test
    selfLink: /oapi/v1/namespaces/test/routes/sqs
  spec:
    host: sqs-test.''' + host + '''.nip.io
    port:
      targetPort: 4576-tcp
    to:
      kind: Service
      name: localstack
      weight: 100
    wildcardPolicy: None
  status:
    ingress:
    - conditions:
      - lastTransitionTime: 2017-07-28T17:49:18Z
        status: "True"
        type: Admitted
      host: sqs-test.''' + host + '''.nip.io
      routerName: router
      wildcardPolicy: None
kind: List
metadata: {}
selfLink: ""
apiVersion: v1
kind: Route
metadata:
  annotations:
    openshift.io/host.generated: "true"
  name: web
  namespace: test
  selfLink: /oapi/v1/namespaces/test/routes/web
spec:
  host: web-test.''' + host + '''.nip.io
  port:
    targetPort: 8080-tcp
  to:
    kind: Service
    name: localstack
    weight: 100
  wildcardPolicy: None
status:
  ingress:
  - conditions:
    - lastTransitionTime: 2017-07-28T17:52:44Z
      status: "True"
      type: Admitted
    host: web-test.''' + host + '''.nip.io
    routerName: router
    wildcardPolicy: None''')
	s1.send('oc create -f /tmp/routes.yaml')
	s1.send('''aws --endpoint-url=http://kinesis-test.''' + host + '''.nip.io kinesis list-streams''')
	s1.interact()
	

if __name__ == '__main__':
	setup()
	pass
