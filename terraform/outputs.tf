output "cluster_endpoint" {
  description = "Endpoint for EKS cluster"
  value       = aws_eks_cluster.eks_cluster.endpoint
}

output "cluster_name" {
  description = "Name of the EKS cluster"
  value       = aws_eks_cluster.eks_cluster.name
}

output "cluster_region" {
  description = "AWS region of the cluster"
  value       = var.aws_region
}

output "cluster_security_group_id" {
  description = "Security group ID for the cluster"
  value       = aws_eks_cluster.eks_cluster.vpc_config[0].cluster_security_group_id
}

output "eks_secrets_kms_key_arn" {
  description = "KMS key used for Kubernetes Secret envelope encryption"
  value       = aws_kms_key.eks_secrets.arn
}
