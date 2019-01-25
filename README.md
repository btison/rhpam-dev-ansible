Ansible playbook for provisioning RHPAM (Business Central + KIE Server + Postgres)

Prerequisites:
* Log in into Openshift as admin user.
* Import image into openshift namespace:
```
$ oc import-image quay.io/btison/rhpam71-kieserver-openshift-gpte:1.1-3 -n openshift --confirm
```
```
$ oc import-image quay.io/btison/rhpam71-businesscentral-openshift-gpte:1.1 -n openshift --confirm
```

To provision:
```
$ ansible-playbook playbooks/pgadmin4.yml -e ocp_user=user1
$ ansible-playbook playbooks/nexus2.yml -e ocp_user=user1
$ ansible-playbook playbooks/rhpam_dev.yml -e ocp_user=user1 -e kieserver_image=rhpam71-kieserver-openshift-gpte -e kieserver_image_tag=1.1-3 -e businesscentral_image=rhpam71-businesscentral-openshift-gpte -e businesscentral_image_tag=1.1  
```