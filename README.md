Ansible playbook for provisioning RHPAM (Business Central + KIE Server + Postgres)

Prerequisites:
* Log in into Openshift as admin user.

Provision:
```
$ ansible-playbook playbooks/pgadmin4.yml -e ocp_user=user1
$ ansible-playbook playbooks/nexus2.yml -e ocp_user=user1
$ ansible-playbook playbooks/rhpam_dev.yml -e ocp_user=user1 -e kieserver_image=rhpam73-kieserver-openshift -e kieserver_image_tag=1.0 -e businesscentral_image=rhpam73-businesscentral-openshift -e businesscentral_image_tag=1.0  
```

Provision for a range of users:
```
$ ansible-playbook playbooks/install.yml -e seq_start=1 -e seq_end=10
```

__Using custom images for Business-Central and KIE Server__
* The `quay.io/btison/rhpam73-kieserver-openshift-gpte:1.0` and `quay.io/btison/rhpam73-businesscentral-openshift-gpte:1.0` are derived from the Red Hat RHPAM 7.3.x images. The images are configured with users and groups required to support the GPTE courses and labs.
* Import image into openshift namespace:
```
$ oc import-image quay.io/btison/rhpam73-kieserver-openshift-gpte:1.0 -n openshift --confirm
```
```
$ oc import-image quay.io/btison/rhpam73-businesscentral-openshift-gpte:1.0 -n openshift --confirm
```
* Provision:
```
$ ansible-playbook playbooks/pgadmin4.yml -e ocp_user=user1
$ ansible-playbook playbooks/nexus2.yml -e ocp_user=user1
$ ansible-playbook playbooks/rhpam_dev.yml -e ocp_user=user1 -e kieserver_image=rhpam73-kieserver-openshift-gpte -e kieserver_image_tag=1.0 -e businesscentral_image=rhpam73-businesscentral-openshift-gpte -e businesscentral_image_tag=1.0
```
* Provision for a range of users:
```
$ ansible-playbook playbooks/install.yml -e seq_start=1 -e seq_end=10 -e kieserver_image=rhpam73-kieserver-openshift-gpte -e kieserver_image_tag=1.0 -e businesscentral_image=rhpam73-businesscentral-openshift-gpte -e businesscentral_image_tag=1.0
```
