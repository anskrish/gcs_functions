all: plan

set:
	rm -f .terraform/terraform.tfstate
	terraform init

plan:
	terraform plan -out=fun.out

apply:
	terraform apply -auto-approve 

destroy:
	terraform destroy -auto-approve
clean:
	rm -f *.tfvars
	rm -f *.out
	rm -rf .terraform*

