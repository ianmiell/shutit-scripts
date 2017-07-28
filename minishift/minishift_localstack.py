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
  creationTimestamp: 2017-07-28T17:35:35Z
  name: restricted
  resourceVersion: "867"
  selfLink: /api/v1/securitycontextconstraintsrestricted
  uid: 299a570a-73bb-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:44:17Z
    name: apigateway
    namespace: test
    resourceVersion: "1221"
    selfLink: /oapi/v1/namespaces/test/routes/apigateway
    uid: 61032a47-73bc-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:48:45Z
    name: cloudformation
    namespace: test
    resourceVersion: "1288"
    selfLink: /oapi/v1/namespaces/test/routes/cloudformation
    uid: 00c21cbc-73bd-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:45:18Z
    name: cloudwatch
    namespace: test
    resourceVersion: "1236"
    selfLink: /oapi/v1/namespaces/test/routes/cloudwatch
    uid: 85391f7b-73bc-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:48:58Z
    name: dynamodb
    namespace: test
    resourceVersion: "1292"
    selfLink: /oapi/v1/namespaces/test/routes/dynamodb
    uid: 088895fc-73bd-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:50:06Z
    name: dynamodbstreams
    namespace: test
    resourceVersion: "1312"
    selfLink: /oapi/v1/namespaces/test/routes/dynamodbstreams
    uid: 30aee2c1-73bd-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:50:52Z
    name: es
    namespace: test
    resourceVersion: "1328"
    selfLink: /oapi/v1/namespaces/test/routes/es
    uid: 4c643d07-73bd-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:50:23Z
    name: firehose
    namespace: test
    resourceVersion: "1318"
    selfLink: /oapi/v1/namespaces/test/routes/firehose
    uid: 3ae1b04d-73bd-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:46:36Z
    name: kinesis
    namespace: test
    resourceVersion: "1256"
    selfLink: /oapi/v1/namespaces/test/routes/kinesis
    uid: b401d134-73bc-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:51:06Z
    name: lambda
    namespace: test
    resourceVersion: "1333"
    selfLink: /oapi/v1/namespaces/test/routes/lambda
    uid: 54a246b8-73bd-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:46:59Z
    name: redshift
    namespace: test
    resourceVersion: "1263"
    selfLink: /oapi/v1/namespaces/test/routes/redshift
    uid: c192bbd1-73bc-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:50:37Z
    name: route53
    namespace: test
    resourceVersion: "1323"
    selfLink: /oapi/v1/namespaces/test/routes/route53
    uid: 43945a97-73bd-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:48:14Z
    name: s3
    namespace: test
    resourceVersion: "1280"
    selfLink: /oapi/v1/namespaces/test/routes/s3
    uid: ee64864f-73bc-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:46:15Z
    name: ses
    namespace: test
    resourceVersion: "1250"
    selfLink: /oapi/v1/namespaces/test/routes/ses
    uid: a737335e-73bc-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:49:42Z
    name: sns
    namespace: test
    resourceVersion: "1305"
    selfLink: /oapi/v1/namespaces/test/routes/sns
    uid: 226938b5-73bd-11e7-8ed8-feafb856dd50
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
    creationTimestamp: 2017-07-28T17:49:18Z
    name: sqs
    namespace: test
    resourceVersion: "1298"
    selfLink: /oapi/v1/namespaces/test/routes/sqs
    uid: 145eefaa-73bd-11e7-8ed8-feafb856dd50
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
resourceVersion: ""
selfLink: ""
apiVersion: v1
kind: Route
metadata:
  annotations:
    openshift.io/host.generated: "true"
  creationTimestamp: 2017-07-28T17:52:44Z
  name: web
  namespace: test
  resourceVersion: "1355"
  selfLink: /oapi/v1/namespaces/test/routes/web
  uid: 8f032a3e-73bd-11e7-8ed8-feafb856dd50
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
