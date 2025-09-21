

# Runbook

## 🛡️ Auto-Quarantine
1. When worker faces CAPTCHA:  
   - Metric `crawler_error_total` increases  
   - Quarantine the worker (pause)  
   - Restart after a cooldown  

## 🔄 Auto-Replace
1. If a node fails or worker pod is stuck:  
   - Drain node:  
     ```bash
     kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
     ```
   - Pods will be rescheduled automatically  
   - Replace node if needed:  
     ```bash
     kubectl delete node <node-name>
     ```
   - Verify service and metrics are healthy  