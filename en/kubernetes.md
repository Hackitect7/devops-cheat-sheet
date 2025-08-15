<style>
  table { table-layout: fixed; width: 100%; }
  td:nth-child(2) code { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }
</style>

# ☸️ Kubernetes and kubectl

> 📘 This cheat sheet is a practical guide to `kubectl` and core Kubernetes objects. It helps you quickly handle day-to-day tasks (resource discovery and filtering, deployment and scaling, debugging and access) without digging through the docs, and apply safe defaults and best practices right away. Use it as an incident aide-mémoire, a pre-release checklist, and a set of ready-to-use YAML snippets for bootstrapping new services. Suitable for both newcomers and experienced engineers—from basic operations to professional techniques.

---

## 📂 Table of contents

- [☸️ Kubernetes and kubectl](#️-kubernetes-and-kubectl)
  - [📂 Table of contents](#-table-of-contents)
  - [🔹 Basic commands](#-basic-commands)
  - [📄 Viewing and filtering resources](#-viewing-and-filtering-resources)
    - [Output formats and JSONPath (for `kubectl get`)](#output-formats-and-jsonpath-for-kubectl-get)
  - [🔧 Managing objects](#-managing-objects)
  - [📈 Scaling and Releases](#-scaling-and-releases)
  - [🧰 Debugging, Access, and Copying](#-debugging-access-and-copying)
  - [🌐 Networking: Service, Ingress, NetworkPolicy](#-networking-service-ingress-networkpolicy)
  - [🗄️ Storage: PV/PVC/StorageClass](#️-storage-pvpvcstorageclass)
    - [YAML snippets: attaching a PVC in a Pod/Deployment](#yaml-snippets-attaching-a-pvc-in-a-poddeployment)
  - [🔐 Configuration \& Secrets](#-configuration--secrets)
    - [YAML snippets: wiring ConfigMap/Secret into a Pod](#yaml-snippets-wiring-configmapsecret-into-a-pod)
  - [🔑 RBAC \& Security](#-rbac--security)
  - [🧪 Resources, Probes, and HPA](#-resources-probes-and-hpa)
    - [YAML snippets: resources and probes (insert into `containers[]`/`spec`)](#yaml-snippets-resources-and-probes-insert-into-containersspec)
  - [🧠 Advanced Commands](#-advanced-commands)
  - [🤖 Automation and Best Practices](#-automation-and-best-practices)
  - [📦 Workloads: Deploy/STS/DS/Job/CronJob](#-workloads-deploystsdsjobcronjob)
  - [📌 YAML Mini-Templates](#-yaml-mini-templates)
    - [Deployment + Service (ClusterIP)](#deployment--service-clusterip)
    - [Ingress (nginx-ingress) with TLS](#ingress-nginx-ingress-with-tls)
    - [PVC + using a volume in a Pod](#pvc--using-a-volume-in-a-pod)
    - [HPA v2 for CPU](#hpa-v2-for-cpu)
    - [NetworkPolicy: deny-all + allow from namespace web](#networkpolicy-deny-all--allow-from-namespace-web)
    - [RBAC: read-only role in a namespace](#rbac-read-only-role-in-a-namespace)
    - [Debug: ephemeral container (via command)](#debug-ephemeral-container-via-command)
  - [💡 kubectl Aliases](#-kubectl-aliases)
    - [Bash: autocompletion + basic set](#bash-autocompletion--basic-set)
    - [Zsh: autocompletion + basic set](#zsh-autocompletion--basic-set)
  - [📚 Additional resources](#-additional-resources)
    - [💡 Tips](#-tips)
    - [🌐 Useful links](#-useful-links)
      - [📘 Official references](#-official-references)
      - [📙 Networking](#-networking)
      - [📗 Scaling and metrics](#-scaling-and-metrics)
      - [📕 Storage](#-storage)
      - [📘 Security and access](#-security-and-access)
      - [📙 Workloads and core objects](#-workloads-and-core-objects)
      - [📗 Local clusters](#-local-clusters)
      - [📕 `kubectl` plugins](#-kubectl-plugins)

---

## 🔹 Basic commands

> **Purpose:** foundational actions to connect to a cluster, inventory objects, and do quick diagnostics—versions, availability, resource types, context switching, lists, details, logs, and built-in help.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl version`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#version) | | **Outputs the `kubectl` client and Kubernetes API server versions. Used to verify connectivity and compatibility** |
|         | `kubectl version --short` | Concise human-readable versions |
|         | `kubectl version --client` | Show client version only (no server call) |
|         | `kubectl version -o yaml` | YAML output for CI/scripts |
| [**`kubectl cluster-info`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#cluster-info) | | **Shows addresses of core cluster services (API server, DNS, etc.). Used for a quick availability check** |
|         | `kubectl cluster-info` | Summary of key services and their URLs |
|         | `kubectl cluster-info dump --all-namespaces` | Collect a diagnostic dump (manifests, events) for debugging |
|         | `kubectl --context prod cluster-info` | Query info for the specified context |
| [**`kubectl api-resources`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#api-resources) | | **Lists supported resource kinds and their short names. Useful to verify CRDs and align manifests** |
|         | `kubectl api-resources` | Basic list of resources (kind, shortnames) |
|         | `kubectl api-resources -o wide` | Add groups/versions and extra columns |
|         | `kubectl api-resources --namespaced=true` | Show only namespaced resources (or `false` for cluster-scoped) |
| [**`kubectl api-versions`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#api-versions) | | **Lists all API groups/versions available in the cluster. Used to reconcile versions referenced in manifests** |
|         | `kubectl api-versions` | Full list of API groups/versions |
|         | `kubectl api-versions \| grep '^autoscaling/'` | Verify `autoscaling/v2` is available (HPA v2) |
|         | `kubectl api-versions \| grep -E '^(apps\|batch)/v1$'` | Ensure stable `apps/v1`, `batch/v1` are present |
| [**`kubectl config`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#config) | | **Manages kubeconfig (clusters, users, contexts). Used to switch environments and the default namespace** |
|         | `kubectl config get-contexts` | List available contexts |
|         | `kubectl config use-context prod` | Switch to the `prod` context |
|         | `kubectl config set-context --current --namespace=dev` | Set `dev` as the default namespace |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Retrieves lists of objects. Baseline command for inventory and initial diagnostics** |
|         | `kubectl get nodes -o wide` | Node status with additional fields (IP, roles) |
|         | `kubectl get all -A` | All core objects across all namespaces |
|         | `kubectl get pods -l app=web -A` | List pods by label selector across all `ns` |
| [**`kubectl describe`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Prints detailed information about a resource: spec, current status, conditions, and related events. Used for diagnostics** |
|         | `kubectl describe node worker-1` | Show roles, taints, readiness conditions, capacity/allocatable, and a pod summary on the node |
|         | `kubectl describe pod web-xyz -n app` | Show containers, images, env vars, probes, restart reasons, and pod events |
|         | `kubectl describe ingress web -n app` | Show routing rules, controller annotations, TLS section, and attached services/paths |
| [**`kubectl logs`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#logs) | | **Prints container stdout/stderr. Used to analyze application behavior and incidents** |
|         | `kubectl logs pod/web-xyz -n app -f` | Continuous stream of current logs (follow) |
|         | `kubectl logs pod/web-xyz -c nginx -n app --since=1h` | Logs of the selected container for a time window |
|         | `kubectl logs -l app=web -c nginx -n app --tail=200 -f` | Logs for all pods by label selector (bulk collection) |
| [**`kubectl explain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#explain) | | **Displays help for API objects and fields: purpose, type, nesting, and supported values** |
|         | `kubectl explain deploy.spec.strategy` | Description of deployment strategies (RollingUpdate/Recreate) and their parameters |
|         | `kubectl explain pod.spec.containers.resources` | Structure and types for `requests` and `limits` |
|         | `kubectl explain service.spec.ports` | Field descriptions for service ports and configuration options |

> ***Notes:***  
> • `-A` shows resources across all namespaces; for targeted selections use labels `-l key=value` and field selectors `--field-selector=...`.  
> • `describe` often includes useful events at the bottom—first clue during failures.  
> • `api-resources` reveals short names usable in `kubectl get/describe`.  
> • To avoid environment mix-ups keep your active context and namespace set via `kubectl config`.

---

## 📄 Viewing and filtering resources

> **Purpose:** get a “state snapshot” of the cluster and quickly filter the required objects; inspect resource details, logs and events; collect usage metrics; choose an appropriate output format and extract targeted data for scripts via JSONPath.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Retrieves lists of objects with filtering and output format options** |
|         | `kubectl get pods -n app -o wide` | List pods in `app` with extended columns (IP, node, etc.) |
|         | `kubectl get pods -l app=web -A` | Filter by labels (label selector) across all namespaces |
|         | `kubectl get pods --field-selector=status.phase=Running -A` | Filter by fields (field selector), e.g., only `Running` |
|         | `kubectl get deploy -w -n app` | “Watch” resource changes in real time (`--watch`) |
| [**`kubectl describe`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Shows detailed spec, current status, and related events of an object** |
|         | `kubectl describe pod web-xyz -n app` | Pod details: containers, probes, environment variables, events |
|         | `kubectl describe node worker-1` | Node state: roles, taints, conditions, capacity/allocatable |
|         | `kubectl describe ingress web -n app` | Routing rules, controller annotations, TLS section |
| [**`kubectl logs`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#logs) | | **Prints container `stdout/stderr` to analyze application behavior** |
|         | `kubectl logs pod/web-xyz -n app -f` | Continuous stream of current logs (`--follow`) |
|         | `kubectl logs pod/web-xyz -c nginx -n app --since=1h` | Logs of the selected container for the last hour |
|         | `kubectl logs -l app=web -c nginx -n app --tail=200 -f` | Logs of all pods by label selector (bulk collection) |
| [**`kubectl get events`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#events) | | **Shows cluster events for temporal diagnostics** |
|         | `kubectl get events -A --sort-by=.lastTimestamp` | Event timeline across all namespaces |
|         | `kubectl get events -n app --field-selector=involvedObject.name=web-xyz` | Events related to a specific object |
|         | `kubectl get events -A --field-selector type=Warning` | Only warnings (if the `type` field is supported) |
| [**`kubectl top`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#top) | | **Shows CPU/memory usage (requires metrics-server installed)** |
|         | `kubectl top pods -n app` | Resource usage by pods in `app` |
|         | `kubectl top nodes` | Summary by nodes (CPU/Memory) |
|         | `kubectl top pods -l app=web -A` | Metrics only for pods with specific labels |
| [**`kubectl explain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#explain) | | **Help for API objects and fields (purpose, type, nesting)** |
|         | `kubectl explain deploy.spec.strategy` | Description of deployment strategies and their parameters |
|         | `kubectl explain pod.spec.containers.resources` | Structure of `requests`/`limits` and value types |
|         | `kubectl explain service.spec.ports` | Service port fields and configuration options |

### Output formats and JSONPath (for `kubectl get`)

> **Purpose:** quickly obtain data in a convenient format for reading, copying into tickets, and subsequent automated processing (scripts/CI).  
> **Useful when:** you need full resource specs, only object names, your own columns, or to extract specific values (e.g., IP, image, status).

**Output formats (for `kubectl get`). Choose the result format for diagnostics and further processing**

| Example | Description |
| ------ | -------- |
| `-o wide` | Extended columns (node, IP, etc.) for convenient reading |
| `-o yaml` / `-o json` | Full object specification—useful for diffs/reviews and incident logs |
| `-o name` | Object names only (handy for pipelines and passing into other commands) |
| `-o custom-columns=NAME:.metadata.name,IP:.status.podIP` | Custom columns for required fields (fits reports/scripts) |
| `-o jsonpath='{..image}'` | Ready for pinpoint value extraction (see JSONPath examples below) |

**JSONPath (within `kubectl get`). Templates to select specific data from an object’s JSON representation**

| Example | Description |
| ------ | -------- |
| `kubectl get pod -n app -o jsonpath='{.items[*].status.podIP}'` | Print IPs of all pods in namespace `app` |
| `kubectl get pod -n app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'` | “pod name → IP” table by lines (easy to copy) |
| `kubectl get pod -n app -o jsonpath='{range .items[*]}{.metadata.name}{" => "}{range .spec.containers[*]}{.image}{" "}{end}{"\n"}{end}'` | Map each pod to the list of its container images |

> ***Notes:***  
> • Label selectors (`-l key=val`) and field selectors (`--field-selector=...`) can be combined; `-A` shows resources across all namespaces.  
> • `--watch/-w` helps observe changes in real time; for a one-time snapshot, remove `-w`.  
> • `describe` often shows key `Events` at the bottom; for a full spec use `-o yaml` instead of `describe`.  
> • Logs: choose the container with `-c`, limit volume with `--since`/`--tail`, collect in bulk by labels with `-l`.  
> • `kubectl top` requires metrics-server; without it, CPU/RAM metrics are unavailable.  
> • Output formats: `-o wide` for reading, `-o name` for pipelines, `-o custom-columns=...` for tabular reports, `-o json|yaml` for machine processing.  
> • JSONPath: wrap expressions in single quotes in bash (`-o jsonpath='{...}'`), escape special characters if needed; handy to extract IPs, images, statuses.  
> • Events are ephemeral and may rotate; sort by time (`--sort-by=.lastTimestamp` or `.eventTime`) and, if needed, filter by object via `--field-selector=involvedObject.*`.

---

## 🔧 Managing objects

> **Purpose:** bring cluster objects to the desired state (apply), preview changes ahead of time (diff), make targeted edits without a full manifest (patch), manage images and metadata (set image/label/annotate), and safely restart workloads (rollout restart).

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl apply`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Creates/updates resources from manifests. Idempotent: converges the cluster to the declared state** |
|         | `kubectl apply -f deploy.yaml` | Apply a single manifest file |
|         | `kubectl apply -k overlays/prod` | Apply a Kustomize directory |
|         | `kubectl apply --server-side -f .` | Server-Side Apply (precise merge on the API server side) |
| [**`kubectl diff`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#diff) | | **Shows differences between the current cluster state and manifests (what will change on `apply`)** |
|         | `kubectl diff -f .` | Compare all manifests in the current folder |
|         | `kubectl diff -k overlays/prod` | Compare the rendered Kustomize result |
|         | `kubectl diff --server-side -f deploy.yaml` | Diff with SSA field-ownership conflicts accounted for |
| [**`kubectl delete`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Deletes resources by type/name, selector, or manifest file** |
|         | `kubectl delete -f deploy.yaml` | Delete resource(s) described in the file |
|         | `kubectl delete svc,ingress -l app=web -n app` | Delete by label selector |
|         | `kubectl delete pod web-xyz --grace-period=0 --force -n app` | Force-delete a pod (use with care) |
| [**`kubectl edit`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#edit) | | **Opens a resource in `$EDITOR` and saves changes back to the cluster** |
|         | `kubectl edit deployment web -n app` | Edit a Deployment |
|         | `kubectl edit configmap app-cm -n app` | Edit a ConfigMap |
|         | `KUBE_EDITOR="code --wait" kubectl edit svc web -n app` | Use a specific editor |
| [**`kubectl patch`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#patch) | | **Partial update of a resource without the full manifest (merge/json/strategic)** |
|         | `kubectl patch deploy web -n app -p '{"spec":{"replicas":3}}' --type=merge` | Merge patch: change replica count |
|         | `kubectl patch deploy web -n app --type=json -p='[{"op":"add","path":"/spec/template/metadata/annotations/checksum","value":"sha256:..."}]'` | JSON patch: add an annotation |
|         | `kubectl patch svc web -n app -p '{"spec":{"sessionAffinity":"ClientIP"}}' --type=merge` | Targeted Service tuning |
| [**`kubectl set image`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#set-image) | | **Changes container image(s) of running workloads. Triggers a new rollout** |
|         | `kubectl set image deploy/web app=repo:v2 -n app` | Update image tag |
|         | `kubectl set image deploy/web app=repo@sha256:… -n app` | Update by digest (immutable) |
|         | `kubectl set image ds/agent agent=org/agent:1.4 -n ops` | Update a DaemonSet |
| [**`kubectl label`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#label) | | **Adds/modifies labels for selection and policy** |
|         | `kubectl label pod web-xyz tier=frontend --overwrite -n app` | Add/update a pod label |
|         | `kubectl label ns app istio-injection=enabled --overwrite` | Label a namespace |
|         | `kubectl label pods -l app=web canary=true -n app` | Bulk by selector |
| [**`kubectl annotate`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#annotate) | | **Adds/modifies annotations (metadata) for operational purposes and triggers** |
|         | `kubectl annotate deploy/web checksum/config=sha256:... --overwrite -n app` | Annotation as a restart trigger on config change |
|         | `kubectl annotate svc web external-dns.alpha.kubernetes.io/hostname=app.example.com -n app` | Annotation for integrations (external-dns, etc.) |
|         | `kubectl annotate pod web-xyz purpose=debug --overwrite -n app` | Temporary marker for debugging |
| [**`kubectl rollout restart`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Restarts workload pods without changing the manifest (creates a new ReplicaSet revision)** |
|         | `kubectl rollout restart deploy/web -n app` | Restart a Deployment |
|         | `kubectl rollout restart daemonset/agent -n ops` | Restart a DaemonSet |
|         | `kubectl rollout status deploy/web -n app` | Track completion of the restart |

> ***Notes:***  
> • In CI/CD, run `kubectl diff` and/or `--dry-run=server` before `apply` to catch schema errors and unexpected changes early.  
> • Prefer **Server-Side Apply**: `apply --server-side --field-manager=<name>`; a single stable `fieldManager` across pipelines reduces conflicts.  
> • Use `--force-conflicts` only deliberately—you overwrite field ownership from other managers.  
> • `patch` types are `merge`/`json`/`strategic`: for CRDs prefer `--type=json` or `merge`; `strategic` works only for built-in types.  
> • With `set image`, prefer digests (`@sha256:…`) for immutability; after changes, monitor `rollout status`.  
> • Always use `--overwrite` with `label`/`annotate`; annotations like `checksum/config=…` are handy as restart triggers.  
> • Use `delete` with selectors carefully; always specify `-n` and context; control cascading: `--cascade=foreground|background|orphan`.  
> • `edit` is convenient for urgent fixes, but changes won’t land in Git—commit the final state back to manifests (GitOps).  
> • After `apply`, inspect the effective spec with `get -o yaml`—admission webhooks may have mutated the object.  
> • For repeatability, standardize the sequence `diff → apply → rollout status/wait` and define explicit timeouts.

---

## 📈 Scaling and Releases

> **Purpose:** manage scaling and release lifecycle—manually change replica counts, observe rollout progress, view history and roll back, temporarily pause/resume updates, safely restart pods without changing the manifest, and enable autoscaling via HPA.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl scale`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#scale) | | **Manually changes `spec.replicas` for horizontal scaling** |
|         | `kubectl scale deploy/web --replicas=3 -n app` | Scale the Deployment to 3 replicas |
|         | `kubectl scale sts/db --replicas=1 -n app` | Scale a StatefulSet (preserves ordering) |
|         | `kubectl scale deploy -l app=web --replicas=0 -n app` | Bulk scaling by label selector |
| [**`kubectl rollout status`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Shows rollout state (waits for new pods to become ready)** |
|         | `kubectl rollout status deploy/web -n app` | Track Deployment rollout progress |
|         | `kubectl rollout status sts/db -n app --timeout=5m` | With timeout for StatefulSet |
|         | `kubectl rollout status ds/agent -n ops` | Check DaemonSet status |
| [**`kubectl rollout history`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Shows revision history (ReplicaSet) for rollbacks and audit** |
|         | `kubectl rollout history deploy/web -n app` | Short revision history |
|         | `kubectl rollout history deploy/web --revision=3 -n app` | Details of a specific revision |
|         | `kubectl get rs -n app -l app=web -o wide` | Related ReplicaSets and their parameters |
| [**`kubectl rollout undo`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Rolls an object back to the previous or a specified revision** |
|         | `kubectl rollout undo deploy/web -n app` | Roll back to the previous revision |
|         | `kubectl rollout undo deploy/web --to-revision=3 -n app` | Roll back to a specific revision |
|         | `kubectl rollout status deploy/web -n app` | Track rollback completion |
| [**`kubectl rollout pause`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Pauses Deployment updates. Used to make multiple changes without immediately recreating pods** |
|         | `kubectl rollout pause deploy/web -n app` | Pause updates of the `web` deployment in namespace `app` |
|         | `kubectl rollout pause deployment -l app=web -n app` | Pause all deployments labeled `app=web` |
|         | `kubectl rollout pause deploy/api -n app` | Pause another deployment before a series of changes |
| [**`kubectl set image`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#set-image) | | **Changes container images of workloads. Often used during a pause** |
|         | `kubectl set image deploy/web app=repo:v2 -n app` | Update `app` container to tag `v2` |
|         | `kubectl set image deploy/web app=repo@sha256:... -n app` | Update image by digest (immutable) |
|         | `kubectl set image deploy/web app=repo:v2 sidecar=side:v1 -n app` | Update multiple containers in one deployment |
| [**`kubectl rollout resume`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Resumes Deployment updates. After changes, triggers a rollout** |
|         | `kubectl rollout resume deploy/web -n app` | Resume updates of the `web` deployment |
|         | `kubectl rollout resume deployment -l app=web -n app` | Resume all deployments labeled `app=web` |
|         | `kubectl rollout status deploy/web -n app` | Verify that the rollout completed successfully |
| [**`kubectl rollout restart`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Creates a new revision and restarts pods without changing the manifest** |
|         | `kubectl rollout restart deploy/web -n app` | Refresh pods (e.g., after ConfigMap/Secret change) |
|         | `kubectl rollout restart ds/agent -n ops` | Restart a DaemonSet |
|         | `kubectl rollout status deploy/web -n app` | Wait for readiness after the restart |
| [**`kubectl autoscale`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#autoscale) | | **Creates/updates an HPA (autoscaling/v1) for CPU-based scaling** |
|         | `kubectl autoscale deploy/web --cpu-percent=60 --min=2 --max=10 -n app` | HPA for a Deployment by CPU |
|         | `kubectl get hpa -n app` | Check the created HPA |
|         | `kubectl delete hpa web -n app` | Delete the HPA *(for memory/custom metrics use `autoscaling/v2` YAML)* |

> ***Notes:***  
> • `scale` and HPA: manual changes to `.spec.replicas` will be overwritten by HPA; for manual control adjust `minReplicas/maxReplicas` or remove the HPA.  
> • Use `rollout status` with `--timeout` as a CI gate; for Deployments configure `progressDeadlineSeconds`.  
> • The `pause → apply/set image → resume` pattern lets you batch multiple edits into a single rollout.  
> • `rollout restart` adds the `kubectl.kubernetes.io/restartedAt` annotation and restarts pods, but does not change the spec.  
> • StatefulSets update and scale in order; for canaries use `updateStrategy.rollingUpdate.partition`, for parallel startup use `podManagementPolicy: Parallel`.  
> • DaemonSets don’t scale by replicas; control updates via `updateStrategy` and `kubectl rollout status ds/...`.  
> • HPA v1 works on CPU; for memory/combined/custom metrics use `autoscaling/v2` YAML and ensure **metrics-server** is installed.  
> • HPA typically won’t scale to zero without external components (e.g., KEDA).  
> • Control deployment strategy parameters: `maxSurge`/`maxUnavailable`, `revisionHistoryLimit`, `PodDisruptionBudget` — this reduces risk of degradation.

---

## 🧰 Debugging, Access, and Copying

> **Purpose:** rapid diagnostics of applications and nodes—enter a container (`exec`), attach to an already running process (`attach`), get local access to services without external exposure (`port-forward`), move files (`cp`), safely debug via ephemeral containers (`debug`), and service nodes and inspect their state (`describe node`, `cordon/drain/uncordon`).

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl exec`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#exec) | | **Runs a command inside a container or opens an interactive shell. Used for application diagnostics** |
|         | `kubectl exec -it pod/web-xyz -n app -- bash` | Open an interactive shell in the container (if `bash` is unavailable, use `sh`) |
|         | `kubectl exec pod/web-xyz -n app -- printenv \| sort` | Run a single command and print the result |
|         | `kubectl exec -it pod/web-xyz -c app -n app -- sh` | Target a specific container in the pod |
| [**`kubectl attach`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#attach) | | **Attaches to the container’s already running process (PID 1). Does not start a new shell** |
|         | `kubectl attach -it pod/web-xyz -n app` | Attach to the container’s main process |
|         | `kubectl attach -it pod/web-xyz -c app -n app` | Attach to a specific container in the pod |
|         | `kubectl attach pod/web-xyz -n app --sigusr1` | Send a signal to the process (if supported) |
| [**`kubectl port-forward`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#port-forward) | | **Forwards a local port to a pod/service port. Useful for local checks without exposing the service externally** |
|         | `kubectl port-forward pod/web-xyz 8080:80 -n app` | Local `localhost:8080` → container port `80` |
|         | `kubectl port-forward svc/web 8443:443 -n app` | Forward to a Service (load-balanced to pods behind it) |
|         | `kubectl port-forward deploy/web 9090:9090 -n app` | Forward to one of the Deployment’s pods |
| [**`kubectl cp`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#cp) | | **Copies files/directories between the local machine and a pod** |
|         | `kubectl cp app/pod:/var/log/app.log ./ -n app` | Copy a file from a pod to the local machine |
|         | `kubectl cp ./config.yml app/pod:/etc/app/config.yml -n app` | Upload a file into a container |
|         | `kubectl cp -c app app/pod:/data ./data -n app` | Specify the container (`-c`) when copying |
| [**`kubectl debug`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#debug) | | **Starts a debug (ephemeral) container alongside the target without restarting the app** |
|         | `kubectl debug pod/web-xyz --image=busybox:1.36 --target=app -n app` | Attach an ephemeral container to the pod and “jump” inside |
|         | `kubectl debug -it pod/web-xyz --image=busybox:1.36 -n app -- bash` | Interactive session in the debug container |
|         | `kubectl debug node/worker-1 -it --image=busybox:1.36` | Debug pod on a specific node for node diagnostics |
| [**`kubectl describe node`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Shows node details: roles, taints, conditions, capacity/allocatable, scheduled pods** |
|         | `kubectl describe node worker-1` | Diagnose scheduling issues or node overload |
|         | `kubectl get nodes -o wide` | Quick overview of IP/roles before deep-dive diagnostics |
|         | `kubectl top nodes` | CPU/memory usage per node (metrics-server required) |
| [**`kubectl cordon`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#cordon) | | **Marks a node as `Unschedulable`. New pods won’t be scheduled there; existing ones stay** |
|         | `kubectl cordon worker-1` | Disallow scheduling on node `worker-1` |
|         | `kubectl cordon worker-1 worker-2` | Mark multiple nodes at once |
|         | `kubectl get nodes` | Verify node status is `SchedulingDisabled` |
| [**`kubectl drain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#drain) | | **Evacuates pods from a node and sets it to `Unschedulable`. Respects PDB; ignores DaemonSet pods** |
|         | `kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data --force --timeout=5m` | Typical drain for node maintenance (deletes `emptyDir`, forces unmanaged pods) |
|         | `kubectl drain worker-1 --grace-period=60 --timeout=10m` | Set graceful termination time for pods and an overall timeout |
|         | `kubectl drain worker-1 --pod-selector='app!=critical' --ignore-daemonsets --delete-emptydir-data --force` | Evacuate only pods matching the selector |
| [**`kubectl uncordon`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#uncordon) | | **Clears the `Unschedulable` mark. Pods can be scheduled on the node again** |
|         | `kubectl uncordon worker-1` | Bring the node back into scheduling |
|         | `kubectl uncordon worker-1 worker-2` | Enable multiple nodes |
|         | `kubectl get nodes -o wide` | Ensure scheduling is allowed |

> ***Notes:***  
> • **`exec` vs `attach`:** `exec` starts a new process (usually a shell) and doesn’t affect PID 1; `attach` “sticks” to PID 1 and depends on how it handles input/signals.  
> • **`port-forward`:** forwards only TCP and listens on `localhost` by default; unstable across pod restarts—use Service/Ingress/LoadBalancer for persistent access.  
> • **`cp`:** uses `tar` under the hood; `tar` must be available in the container, otherwise copy via `exec ... -- sh -c 'cat > /path/file'`; note that a trailing `/` in paths changes copy semantics.  
> • **`debug` (ephemeral containers):** do not mount volumes or ports, but share namespaces with the target—great for installing diagnostic tools without changing the image; `kubectl debug node/...` creates a privileged pod for node debugging—requires appropriate RBAC.  
> • **`describe node`:** check `Taints`, `Conditions`, and placed pods; for metrics use `kubectl top nodes` (metrics-server required).  
> • **`cordon`/`drain`/`uncordon`:** check `PodDisruptionBudget` first (`kubectl get pdb -A`); use `--ignore-daemonsets` and set `--grace-period/--timeout`; `drain` only deletes controller-managed pods—standalone pods require `--force`.  
> • In production avoid “manual” tweaks inside containers; codify findings in manifests and apply via a GitOps pipeline.

---

## 🌐 Networking: Service, Ingress, NetworkPolicy

> **Purpose:** verify service reachability, understand where traffic flows (L4/L7), and see which NetworkPolicies are in effect. Useful for “doesn’t open,” 404/502, timeouts, and NetworkPolicy isolation.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl get svc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **List Services and their exposure parameters (type, IP, ports)** |
|         | `kubectl get svc web -n app -o wide` | View type (ClusterIP/NodePort/LB), IP, and ports of Service `web` |
|         | `kubectl get svc -l app=web -n app` | Filter Services by label `app=web` |
|         | `kubectl get svc web -n app -o yaml` | Full Service spec for diagnostics/review |
| [**`kubectl get endpoints`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Shows the actual backend addresses (IP:port) of pods targeted by the Service** |
|         | `kubectl get endpoints web -n app -o wide` | View IPs and ports of pods behind Service `web` |
|         | `kubectl get endpoints -l app=web -n app` | List endpoints for Services labeled `app=web` |
|         | `kubectl get endpoints web -n app -o yaml` | Full Endpoints spec for detailed diagnostics |
| [**`kubectl get endpointslices`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Shows EndpointSlice—a scalable representation of the same backend addresses** |
|         | `kubectl get endpointslices -n app` | List all EndpointSlices in namespace `app` |
|         | `kubectl get endpointslices -l kubernetes.io/service-name=web -n app -o yaml` | Slices related to Service `web`, with details |
|         | `kubectl get endpointslices -n app -o wide` | Brief summary of addresses/ports in slices |
| [**`kubectl describe ingress`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **L7 routing details: hosts/paths, controller annotations, TLS** |
|         | `kubectl describe ingress web -n app` | Rules and backend Services for Ingress `web` |
|         | `kubectl get ingress -A` | Quick overview of all Ingresses across all namespaces |
|         | `kubectl get ingress web -n app -o yaml` | Check annotations (timeouts, body size, etc.) |
| [**`kubectl exec`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#exec) | | **Runs a command inside a container. Used for in-cluster network checks (HTTP/DNS) from a pod** |
|         | `kubectl exec -it pod/busy -n app -- curl -sS http://web:80/healthz` | Check HTTP reachability of Service `web` by name |
|         | `kubectl exec -it pod/busy -n app -- wget -qO- http://10.0.0.5:8080/metrics` | Direct check by Pod IP/port |
|         | `kubectl exec -it pod/busy -n app -- nslookup web` | Check the Service DNS name (service discovery) |
| [**`kubectl get networkpolicy`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Shows a list of NetworkPolicies and their brief parameters** |
|         | `kubectl get networkpolicy -A` | All NetworkPolicies across all namespaces |
|         | `kubectl get netpol -n app -o wide` | Useful columns for policies in `app` |
|         | `kubectl get netpol allow-from-web -n db -o yaml` | Full spec of a specific policy |
| [**`kubectl describe networkpolicy`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Shows selectors, directions (`Ingress/Egress`), and ports in detail** |
|         | `kubectl describe networkpolicy allow-from-web -n db` | Analyze rules: from where, to where, which ports |
|         | `kubectl describe netpol -n app` | Details of all policies in namespace `app` |
|         | `kubectl get events -n db --field-selector=involvedObject.kind=NetworkPolicy` | Related events (if any) for diagnostics |

> ***Notes:***  
> • **Service ↔ Endpoints/EndpointSlice**: a regular Service considers only *Ready* pods; to publish not-ready pods use `publishNotReadyAddresses: true`.  
> • **Headless Service (`ClusterIP: None`)**: does not receive a virtual IP; DNS returns pod A records—handy for STS and direct connections.  
> • **ExternalName**: has no Endpoints at all; it’s a DNS alias to an external FQDN—verify via `kubectl get svc ... -o yaml`.  
> • **LoadBalancer/NodePort**: external access appears when `.status.loadBalancer` has an IP/hostname; `externalTrafficPolicy: Local` preserves the source IP but requires at least one *Ready* pod on the node receiving traffic.  
> • **NodePort range**: defaults to `30000–32767` but can be overridden in cluster configuration.  
> • **Ingress**: works only if a controller is installed; verify `ingressClassName`/class, controller-specific annotations, and TLS secret validity.  
> • **DNS**: Service FQDN is `<svc>.<ns>.svc.cluster.local`; headless Services return pod A records; for debugging, run `nslookup/dig` from a pod.  
> • **NetworkPolicy**: policies are additive and enforced only if the CNI supports them; start with `default-deny` and then add *precise* allow rules.  
> • **L7 diagnostic chain**: `Ingress → Service → Endpoints/EndpointSlice → Pod readiness`—a missing link leads to 404/502/timeouts.

---

## 🗄️ Storage: PV/PVC/StorageClass

> **Purpose:** quickly see available classes/volumes, create or expand a PVC, understand `Pending`/binding causes and common pitfalls.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl get sc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Show available StorageClasses and settings** |
|         | `kubectl get sc` | List SCs and the `(default)` mark on the default class |
|         | `kubectl get sc <name> -o yaml` | Check `allowVolumeExpansion`, provisioner parameters and annotations |
|         | `kubectl get sc -o custom-columns=NAME:.metadata.name,DEFAULT:.metadata.annotations['storageclass.kubernetes.io/is-default-class'],BINDING:.volumeBindingMode` | Overview of the default class and binding mode (`WaitForFirstConsumer`/`Immediate`) |
| [**`kubectl get pv`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **View PVs and key fields** |
|         | `kubectl get pv -o wide` | Status, size, `RECLAIM POLICY`, bound PVC |
|         | `kubectl get pv -o custom-columns=NAME:.metadata.name,CLAIM:.spec.claimRef.name,SC:.spec.storageClassName,STATUS:.status.phase` | Custom columns for binding audit |
|         | `kubectl get pv <pv> -o jsonpath='{.spec.persistentVolumeReclaimPolicy}'` | See `Delete`/`Retain` for a specific PV |
| [**`kubectl get pvc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Show PVC status and parameters** |
|         | `kubectl get pvc -n app -o wide` | Status (`Pending/Bound`), size and StorageClass |
|         | `kubectl get pvc data -n app -w` | Watch status changes (watch) |
|         | `kubectl get pvc data -n app -o jsonpath='{.status.capacity.storage}'` | Actual size after expansion |
| [**`kubectl apply`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Create objects from a manifest (for a PVC—request a volume of the desired size/mode)** |
|         | `kubectl apply -f pvc.yaml` | Create a PVC from a manifest |
|         | `kubectl apply --dry-run=server -f pvc.yaml` | Validate against the API server before applying |
|         | `kubectl apply --server-side -f pvc.yaml` | Apply with SSA for correct field merge |
| [**`kubectl describe pvc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **PVC details and related events (diagnosing `Pending`)** |
|         | `kubectl describe pvc data -n app` | Reasons for not bound, SC/size/topology mismatch |
|         | `kubectl describe pv <pv-name>` | Check `accessModes`/`capacity`/PV labels alignment |
|         | `kubectl get events -n app --field-selector=involvedObject.name=data` | Events related to PVC `data` |
| [**`kubectl patch pvc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#patch) | | **Change PVC size (if the SC supports expansion)** |
|         | `kubectl patch pvc data -n app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'` | Increase the PVC to `20Gi` |
|         | `kubectl patch pvc data -n app --type=json -p='[{"op":"replace","path":"/spec/resources/requests/storage","value":"30Gi"}]'` | Increase via JSON patch |
|         | `kubectl get pvc data -n app -w` | Observe `FileSystemResizePending/Bound` statuses |
| [**`kubectl patch pv`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#patch) | | **Change the PV reclaim policy** |
|         | `kubectl patch pv <pv> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'` | Keep data after PVC deletion |
|         | `kubectl patch pv <pv> -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'` | Revert to deleting the PV along with data |
|         | `kubectl get pv <pv> -o jsonpath='{.spec.persistentVolumeReclaimPolicy}'` | Check the current policy |
| [**`kubectl delete pvc`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Delete a PVC** |
|         | `kubectl delete pvc data -n app` | Behavior with data depends on `reclaimPolicy` and the driver |
|         | `kubectl delete pvc -l app=db -n app` | Bulk delete by label |
|         | `kubectl delete pvc data -n app --wait=false` | Do not wait for the operation to complete |
| [**`kubectl krew`**](https://krew.sigs.k8s.io/) | | **Manage plugins for `kubectl`** |
|         | `kubectl krew install df-pv` | Install plugin to view PV usage |
|         | `kubectl krew install neat` | Install plugin to “clean” YAML from managed fields |
| [**`kubectl df-pv`**](https://github.com/yashbhutwala/kubectl-df-pv) | | **Quick disk usage summary for PVC/PV** |
|         | `kubectl df-pv -n app` | Show usage for namespace `app` |
| [**`kubectl neat`**](https://github.com/itaysk/kubectl-neat) | | **Shows “clean” YAML without managed fields** |
|         | `kubectl get pvc -n app -o yaml \| kubectl neat` | Convenient for review and documentation |

### YAML snippets: attaching a PVC in a Pod/Deployment

| Snippet | Purpose |
| -------- | ---------- |
| `volumeMounts: [{ name: data, mountPath: /data }]` | Mount point of the volume in the container |
| `volumes: [{ name: data, persistentVolumeClaim: { claimName: data } }]` | Bind a PVC to a Pod |
| `securityContext: { fsGroup: 1000 }` | Permissions on the mounted volume (if needed) |

> ***Notes:***  
> • `volumeBindingMode` in the StorageClass: `WaitForFirstConsumer` delays PV binding until pod scheduling—a common cause of `Pending` with zone/topology mismatch.  
> • `RWX` requires an appropriate driver/filesystem (e.g., NFS/CephFS); many block CSI drivers support only `RWO`.  
> • PVCs can usually **only be increased**; shrinking is not supported by most drivers and may cause data loss.  
> • Volume expansion may require a pod restart or filesystem resize; watch `FileSystemResizePending/Bound` stages.  
> • The default class is annotated with `storageclass.kubernetes.io/is-default-class: "true"`.  
> • Dynamic provisioning usually creates PVs with `reclaimPolicy: Delete`; static PVs often use `Retain`.  
> • For `volumeMode: Block`, behavior and expansion procedures differ from filesystem volumes—check your CSI documentation.

---

## 🔐 Configuration & Secrets

> **Purpose:** quickly create/view ConfigMaps/Secrets and wire them into Pods correctly; when needed — safely decode values for diagnostics.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl create configmap`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-configmap) | | **Creates a ConfigMap from literals, files, or an env file** |
|         | `kubectl create configmap app-cm --from-literal=LOG=info -n app` | Create from a key/value pair |
|         | `kubectl create configmap app-cm --from-file=config.yml -n app` | Create from a file/directory |
|         | `kubectl create configmap env-cm --from-env-file=.env -n app` | Create from a `.env` file |
| [**`kubectl create secret generic`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-secret) | | **Creates a generic Secret from literals/files** |
|         | `kubectl create secret generic app-secret --from-literal=PASS=123 -n app` | From a literal (value will be base64 inside the cluster) |
|         | `kubectl create secret generic tls-extra --from-file=cert.pem --from-file=key.pem -n app` | From files |
|         | `kubectl create secret generic cfg --from-file=config=conf.yml -n app` | Set a key name (`config`) for the file |
| [**`kubectl create secret tls`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-secret) | | **Creates a TLS Secret from a `--cert/--key` pair** |
|         | `kubectl create secret tls site-tls --cert=cert.pem --key=key.pem -n app` | TLS for Ingress/client connections |
|         | `kubectl get secret site-tls -n app -o yaml` | Verify type `kubernetes.io/tls` and keys `tls.crt/tls.key` |
| [**`kubectl get secret`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Fetch Secrets and their specs. Suitable for `-o yaml/json/jsonpath`** |
|         | `kubectl get secrets -n app` | List Secrets in the namespace |
|         | `kubectl get secret app-secret -n app -o yaml` | Full specification; values are in `.data` (base64) |
|         | `kubectl get secret app-secret -n app -o jsonpath='{.data}'` | Show all Secret keys (values in base64) |
|         | `kubectl get secret app-secret -n app -o jsonpath='{.data.PASS}' \| base64 -d; echo` | Decode the `PASS` key value |
|         | `kubectl get secret app-secret -n app -o jsonpath="{.data.\*}" \| tr ' ' '\n' \| base64 -d` | Decode all values (one per line) |
| [**`kubectl describe secret`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Human-readable summary: type and list of keys (without values)** |
|         | `kubectl describe secret app-secret -n app` | Secret type and key list |
|         | `kubectl describe secrets -n app` | Short info for all Secrets in the namespace |
|         | `kubectl get events -n app --field-selector=involvedObject.kind=Secret,involvedObject.name=app-secret` | Related events (if recorded) |
| [**`kubectl delete`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Delete ConfigMap/Secret** |
|         | `kubectl delete secret app-secret -n app` | Delete a Secret |
|         | `kubectl delete configmap app-cm -n app` | Delete a ConfigMap |

### YAML snippets: wiring ConfigMap/Secret into a Pod

| Snippet | Purpose |
| -------- | ---------- |
| `envFrom: [ { configMapRef: { name: app-cm } }, { secretRef: { name: app-secret } } ]` | Mount all key/value pairs as environment variables |
| `env: [ { name: LOG_LEVEL, valueFrom: { configMapKeyRef: { name: app-cm, key: LOG } } }, { name: DB_PASS, valueFrom: { secretKeyRef: { name: app-secret, key: PASS } } } ]` | Pull specific keys from CM/Secret into env |
| `volumes: [ { name: tls, secret: { secretName: site-tls } } ]` | Define a secret volume in PodSpec |
| `volumeMounts: [ { name: tls, mountPath: /etc/tls, readOnly: true } ]` | Mount the secret volume in a container |
| `{"apiVersion":"v1","kind":"Secret","metadata":{"name":"app-secret"},"type":"Opaque","stringData":{"PASS":"123"}}` | Example Secret using stringData without manual base64 |

> ***Notes:***  
> • Secrets are base64-encoded, not encrypted; enable Encryption at Rest at the cluster level (KMS).  
> • For GitOps use `stringData` and external encryption (Sealed Secrets, SOPS, KMS).  
> • Avoid passing secrets via `env` when possible: they can appear in `/proc/<pid>/environ` and logs; mounting as a readOnly volume is safer.  
> • Set `immutable: true` for stable ConfigMaps/Secrets — reduces accidental updates and kubelet churn.  
> • Single object size is limited to ≈1 MiB; split large cert chains or store outside the cluster.  
> • Use correct types: `kubernetes.io/tls` (keys `tls.crt`/`tls.key`), `kubernetes.io/dockerconfigjson` (`.dockerconfigjson`) — this simplifies integrations.  
> • Grant narrow RBAC for Secret access and namespaces; audit `get/list/watch` operations.  
> • Decode values only on trusted machines; don’t publish `kubectl get secret -o yaml` to shared logs.  
> • For secret rotation, version keys and use checksum annotations on the PodTemplate to trigger pod restarts.  
> • A Secret is only accessible within its namespace; provide a separate mechanism or duplicate for cross-namespace sharing.

---

## 🔑 RBAC & Security

> **Purpose:** determine “who you are” in the cluster, check permissions for actions, view/assign roles and bindings, and verify access by impersonating another subject.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl auth whoami`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#auth) | | **Shows the current user/groups from kubeconfig (or when impersonating)** |
|         | `kubectl auth whoami` | Current subject and its groups |
|         | `kubectl auth whoami --as=system:serviceaccount:app:deployer` | As service account `app/deployer` |
|         | `kubectl auth whoami --as-group=devs --as-group=qa` | Add groups to test a scenario |
| [**`kubectl auth can-i`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#auth) | | **Check RBAC permissions for an action on a resource** |
|         | `kubectl auth can-i create deploy -n app` | Whether you can create a Deployment in `app` |
|         | `kubectl auth can-i --list -n app` | List all allowed operations in `app` |
|         | `kubectl auth can-i get secrets --namespace app --resource-name app-secret` | Check access to a specific object |
| [**`kubectl get role`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **List roles in a namespace** |
|         | `kubectl get role -n app` | Overview of roles in `app` |
|         | `kubectl get role pod-reader -n app -o yaml` | Full specification of the `pod-reader` role |
| [**`kubectl get rolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **List role bindings in a namespace** |
|         | `kubectl get rolebinding -n app` | Overview of bindings in `app` |
|         | `kubectl get rolebinding view-user -n app -o yaml` | Full specification of the `view-user` binding |
| [**`kubectl get clusterrole`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **List cluster roles (cluster-wide scope)** |
|         | `kubectl get clusterrole -o wide` | Extended output for roles |
|         | `kubectl get clusterrole view -o yaml` | Full specification of the `view` role |
| [**`kubectl get clusterrolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **List cluster role bindings** |
|         | `kubectl get clusterrolebinding` | Overview of cluster role bindings |
|         | `kubectl get clusterrolebinding -o wide` | Who is granted which cluster roles |
|         | `kubectl get clusterrolebinding devs-read -o yaml` | Full specification of the `devs-read` binding |
| [**`kubectl describe role`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Details of a role in a namespace** |
|         | `kubectl describe role pod-reader -n app` | Rules of the `pod-reader` role in `app` |
|         | `kubectl describe role -n app` | All roles with details in `app` |
|         | `kubectl get role pod-reader -n app -o yaml` | Role YAML for review |
| [**`kubectl describe rolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Details of role bindings in a namespace** |
|         | `kubectl describe rolebinding view-user -n app` | Who gets which role |
|         | `kubectl describe rolebinding -n app` | All bindings with details in `app` |
|         | `kubectl get rolebinding view-user -n app -o yaml` | Binding YAML for review |
| [**`kubectl describe clusterrole`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Details of a cluster role** |
|         | `kubectl describe clusterrole view` | Rules of the `view` role |
|         | `kubectl describe clusterrole admin` | Rules of the `admin` role |
|         | `kubectl get clusterrole view -o yaml` | YAML of the `view` role |
| [**`kubectl describe clusterrolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Details of cluster role bindings** |
|         | `kubectl describe clusterrolebinding devs-read` | Who is granted the `view` role (example) |
|         | `kubectl describe clusterrolebinding` | All cluster bindings with details |
|         | `kubectl get clusterrolebinding devs-read -o yaml` | YAML of the `devs-read` binding |
| [**`kubectl create rolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-rolebinding) | | **Bind a Role/ClusterRole to a user/group/SA in a namespace** |
|         | `kubectl create rolebinding view-user --clusterrole=view --user=alice@example.com -n app` | Grant `view` to a user in `app` |
|         | `kubectl create rolebinding edit-devs --clusterrole=edit --group=devs -n app` | Grant `edit` to the `devs` group |
|         | `kubectl create rolebinding deployer-sa --clusterrole=edit --serviceaccount=app:deployer -n app` | Grant `edit` to the `app/deployer` service account |
| [**`kubectl create clusterrolebinding`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-clusterrolebinding) | | **ClusterRole binding — applies across all namespaces** |
|         | `kubectl create clusterrolebinding audit-admin --clusterrole=cluster-admin --user=security@example.com` | Full admin rights to a user |
|         | `kubectl create clusterrolebinding devs-read --clusterrole=view --group=devs` | Cluster-wide read for a group |
|         | `kubectl create clusterrolebinding sa-ci --clusterrole=edit --serviceaccount=ci:runner` | `edit` for SA `ci/runner` across all ns |
| [**`kubectl create role`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-role) | | **Create a Role with required verbs in a namespace** |
|         | `kubectl create role pod-reader --verb=get,list,watch --resource=pods -n app` | Read-only Pods role in `app` |
|         | `kubectl create role secret-reader --verb=get --resource=secrets -n app` | Secret read role |
|         | `kubectl get role pod-reader -n app -o yaml` | Verify the created role |
| [**`kubectl create clusterrole`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create-clusterrole) | | **Create a ClusterRole (cluster-wide scope)** |
|         | `kubectl create clusterrole ns-reader --verb=get,list --resource=namespaces` | Read `namespaces` resources |
|         | `kubectl get clusterrole ns-reader -o yaml` | Verify role rules |
|         | `kubectl delete clusterrole ns-reader` | Delete the role if needed |
| [**`kubectl auth can-i`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#auth) | | **Check RBAC permissions for an action on a resource** |
|         | `kubectl auth can-i create deploy -n app` | Whether you can create a Deployment in `app` |
|         | `kubectl auth can-i --list -n app` | List all allowed operations in `app` |
|         | `kubectl auth can-i get pods --as alice@example.com -n app` | Check access by impersonating another subject |

> ***Notes:***  
> • **Role** and **RoleBinding** are namespace-scoped; **ClusterRole** and **ClusterRoleBinding** are cluster-wide.  
> • A **RoleBinding** can bind either a `Role` or a `ClusterRole` within a specific namespace.  
> • A service account identity is `system:serviceaccount:<ns>:<name>`.  
> • `can-i --list` gives a quick overview; for precise checks against a specific object use `--resource-name`.  
> • For narrow grants, use `resourceNames` in role rules — this limits access to specific objects.  
> • Aggregated ClusterRoles are composed via labels (`rbac.authorization.k8s.io/aggregate-to-*`) — convenient for extending the standard `view/edit/admin` in your org.

---

## 🧪 Resources, Probes, and HPA

> **Purpose:** set container resource limits, configure readiness/liveness checks, and enable autoscaling by metrics.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl top`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#top) | | **Show current CPU/memory usage metrics (requires metrics-server)** |
|         | `kubectl top pods -n app` | Pod metrics in the `app` namespace |
|         | `kubectl top pod web-xyz -n app --containers` | Per-container metrics inside the pod |
|         | `kubectl top nodes` | Node summary |
| [**`kubectl set resources`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#set-resources) | | **Change `requests/limits` for Deployment/StatefulSet/Job, etc** |
|         | `kubectl set resources deploy/web -n app --requests=cpu=200m,memory=128Mi --limits=cpu=500m,memory=256Mi` | Set resources for the deployment’s containers |
|         | `kubectl set resources deploy -l app=web -n app --requests=cpu=300m --limits=cpu=1` | Bulk by label selector |
|         | `kubectl set resources sts/db -n app --limits=memory=2Gi` | Memory limit only for the StatefulSet |
|         | `kubectl set resources deploy/web -c app -n app --requests=cpu=200m --limits=cpu=1` | Change resources only for the `app` container in the deployment |
| [**`kubectl autoscale`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#autoscale) | | **Create/update HPA (v1) based on CPU** |
|         | `kubectl autoscale deploy/web --cpu-percent=60 --min=2 --max=10 -n app` | CPU-based HPA for the deployment |
|         | `kubectl autoscale deploy/api --cpu-percent=75 --min=3 --max=15 -n app` | Another target, different limits |
| [**`kubectl get hpa`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **List/spec of HPAs** |
|         | `kubectl get hpa -n app` | All HPAs in the namespace |
|         | `kubectl get hpa web -n app -o yaml` | Full specification of HPA `web` |
|         | `kubectl get hpa web -n app -w` | Watch changes of metrics/replicas |
| [**`kubectl describe hpa`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Details: current metrics, target, scaling state** |
|         | `kubectl describe hpa web -n app` | Diagnostics: what the HPA sees and why it scales/doesn’t scale |
|         | `kubectl describe hpa -n app` | All HPAs in the namespace |
|         | `kubectl get events -n app --field-selector=involvedObject.kind=HorizontalPodAutoscaler` | Related events (if recorded) |
| [**`kubectl delete hpa`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Delete a Horizontal Pod Autoscaler** |
|         | `kubectl delete hpa web -n app` | Disable HPA for the `web` deployment |
|         | `kubectl delete hpa --all -n app` | Delete all HPAs in the namespace |
|         | `kubectl get hpa -n app` | Verify they are removed |

### YAML snippets: resources and probes (insert into `containers[]`/`spec`)

| Fragment | Purpose |
| -------- | ------- |
| `resources: { requests: { cpu: "100m", memory: "128Mi" }, limits: { cpu: "500m", memory: "256Mi" } }` | Basic QoS and protection from OOM/throttling |
| `readinessProbe: { httpGet: { path: "/", port: 80 }, periodSeconds: 5, initialDelaySeconds: 3 }` | Readiness to accept traffic (affects Service/Ingress) |
| `livenessProbe: { tcpSocket: { port: 80 }, initialDelaySeconds: 10, periodSeconds: 10, failureThreshold: 3 }` | Auto-recover the container when it “hangs” |
| `startupProbe: { httpGet: { path: "/healthz", port: 8080 }, failureThreshold: 30, periodSeconds: 5 }` | Gives the app time to start before checking liveness |
| `{"apiVersion":"autoscaling/v2","kind":"HorizontalPodAutoscaler","metadata":{"name":"web","namespace":"app"},"spec":{"scaleTargetRef":{"apiVersion":"apps/v1","kind":"Deployment","name":"web"},"minReplicas":2,"maxReplicas":10,"metrics":[{"type":"Resource","resource":{"name":"cpu","target":{"type":"Utilization","averageUtilization":60}}}]}}` | HPA v2 by CPU example (equivalent to `kubectl autoscale`) |

> ***Notes***:  
> • QoS classes: **Guaranteed** (requests=limits for all containers), **Burstable** (partially set), **BestEffort** (no requests/limits).  
> • `kubectl autoscale` manages HPA v1 (CPU). For memory/combined/custom metrics use `autoscaling/v2` YAML with `metrics`.  
> • **metrics-server** is required for `kubectl top`/HPA to work.  
> • While `startupProbe` is active, `liveness/readiness` checks are ignored — this is normal for long app startups.  
> • Units: CPU in millicores (`100m` = 0.1 vCPU), memory — `Mi/Gi`; it’s safer to quote values in Helm templates.  
> • HPA modifies `.spec.replicas`; manual `scale` will be overridden by HPA — adjust `minReplicas/maxReplicas` or temporarily delete the HPA.  
> • For memory/custom metrics use HPA **autoscaling/v2** and ensure there is a metrics provider (metrics-server/Prometheus Adapter).  
> • Overly aggressive `livenessProbe` leads to restarts; start with conservative timings and increase `failureThreshold`.

---

## 🧠 Advanced Commands

> **Purpose:** safe production changes and diagnostics—server-side validation, diff, precise merge (SSA), waiting for conditions, deep help, and raw endpoints.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl apply`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Apply manifests, including via Server-Side Apply** |
|         | `kubectl apply --server-side -f .` | Precise merge on the API server side (SSA) |
|         | `kubectl apply --server-side --field-manager=gitops -f .` | Explicit field manager for GitOps workflows |
|         | `kubectl apply -f . --prune -l app=web` | Prune labeled resources not present in the current manifest set |
| [**`kubectl diff`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#diff) | | **Show differences between the cluster and manifests before applying** |
|         | `kubectl diff -f .` | Diff files in the directory |
|         | `kubectl diff --server-side -f .` | Diff considering SSA rules |
|         | `kubectl diff -k overlays/prod` | Diff of a kustomize overlay render |
| [**`kubectl wait`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#wait) | | **Wait for a condition on a resource** |
|         | `kubectl wait deploy/web -n app --for=condition=available --timeout=90s` | Wait until the Deployment is available |
|         | `kubectl wait job/batch-1 -n app --for=condition=complete --timeout=10m` | Wait until the Job is complete |
|         | `kubectl wait --for=delete pod/web-xyz -n app --timeout=60s` | Wait until the object is deleted |
| [**`kubectl kustomize`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#kustomize) | | **Render final YAML from an overlay** |
|         | `kubectl kustomize overlays/prod` | Preview what will be applied |
|         | `kubectl apply -k overlays/prod` | Apply the overlay without Helm |
|         | `kubectl diff -k overlays/prod` | Check changes before applying |
| [**`kubectl explain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#explain) | | **Deep help for API fields** |
|         | `kubectl explain deployment.spec --recursive` | Full tree of fields and types |
|         | `kubectl explain hpa.spec.metrics` | Structure of HPA v2 metrics |
|         | `kubectl explain service.spec.sessionAffinity` | Details of a specific field |
| [**`kubectl get --raw`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Request low-level API server endpoints** |
|         | `kubectl get --raw /healthz` | Basic API health check |
|         | `kubectl get --raw /metrics` | API server metrics in Prometheus format |
|         | `kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes` | Resource metrics from metrics-server |
| [**`kubectl auth reconcile`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#auth) | | **Idempotently reconcile RBAC to the state from YAML** |
|         | `kubectl auth reconcile -f rbac.yaml` | Create/update roles and bindings from a file |
|         | `kubectl auth reconcile -f rbac.yaml --remove-extra-permissions` | Remove extra permissions not specified in YAML |
|         | `kubectl auth can-i --list -n app` | Quick rights check after reconcile |
| [**`kubectl config`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#config) | | **Manage contexts/namespaces to avoid targeting the wrong environment** |
|         | `kubectl config view --minify` | Show active context and namespace |
|         | `kubectl config get-contexts` | List available contexts |
|         | `kubectl config use-context prod` | Switch to the `prod` context |
|         | `kubectl config set-context --current --namespace=app` | Set default namespace for the current context |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Filter with selectors to precisely pick objects** |
|         | `kubectl get pods -l 'app in (web,api)' -n app` | Label filter with a set of values |
|         | `kubectl get pods --field-selector=status.phase=Running -A` | Filter by status field |
|         | `kubectl get svc -l tier=frontend -A` | Quickly select services by role |

> ***Notes:***  
> • **SSA:** use the same `--field-manager` across all pipelines, otherwise you’ll get field ownership conflicts.  
> • **`--force-conflicts`:** use only deliberately — you will overwrite someone else’s field owner.  
> • **Prune:** always scope with a clear label `-l team=…/app=…` — without it you can delete “foreign” resources.  
> • **`dry-run=server`** beats client: it validates CRD schemas and admission validators.  
> • **`diff`** before apply is a must in prod, especially with SSA.  
> • **`wait`** with a timeout and an exact condition (`available/complete/deleted`), otherwise a script may hang.  
> • **`get --raw`** depends on enabled APIs and permissions; not all clusters expose the same endpoints.

---

## 🤖 Automation and Best Practices

> **Purpose:** resilient pipelines and safe releases—validation, diff, waiting, controlled rollouts, and predictable artifacts.

| Command | Example | Description |
| ------- | ------ | -------- |
| [**`kubectl apply --dry-run=server`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Validate manifests against the API server without persisting** |
|         | `kubectl apply --dry-run=server -f .` | Validate a manifest directory in CI |
|         | `kubectl apply --dry-run=server -k overlays/prod` | Validate an environment overlay |
|         | `kubectl apply --dry-run=server -f deploy.yaml -o yaml` | Get the resulting spec for review |
| [**`kubectl rollout status`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Pipeline gate: wait for rollout to complete** |
|         | `kubectl rollout status deploy/web -n app` | Wait for the deployment to become ready after apply |
|         | `kubectl rollout status sts/db -n app --timeout=10m` | Timeout for stateful workloads |
|         | `kubectl rollout history deploy/web -n app` | Inspect revisions before rollback |
| [**`kubectl set image`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#set-image) | | **Immutable images for repeatable releases** |
|         | `kubectl set image deploy/web app=repo@sha256:... -n app` | Pin by digest instead of a floating tag |
|         | `kubectl rollout status deploy/web -n app` | Verify rollout success |
|         | `kubectl rollout undo deploy/web -n app` | Quick rollback on issues |
| [**`kubectl annotate`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#annotate) | | **Explicit restart triggers on config/secret changes** |
|         | `kubectl annotate deploy/web checksum/config=sha256:... -n app --overwrite` | Update the annotation and start a new rollout |
|         | `kubectl rollout status deploy/web -n app` | Wait for restart to complete |
|         | `kubectl get deploy web -n app -o yaml` | Ensure the annotation is on the PodTemplate |
| [**`kubectl label`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#label) | | **Selective releases and queries via labels** |
|         | `kubectl label deploy/web track=canary -n app --overwrite` | Mark the target for canary routing |
|         | `kubectl get pods -l track=canary -n app` | Verify replicas are labeled |
|         | `kubectl delete pods -l track=canary -n app` | Operate only on the target group |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Automation via output formats** |
|         | `kubectl get pods -l app=web -n app -o name` | Fetch names only for pipelines |
|         | `kubectl get hpa -n app -o jsonpath='{.items[*].status.currentMetrics[*].resource.current.averageUtilization}'` | Extract metrics for decision making |
|         | `kubectl get events -A --sort-by=.lastTimestamp` | Event timeline for quick release diagnostics |
| [**`kubectl rollout pause\|resume`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#rollout) | | **Batch multiple changes and control when rollout starts** |
|         | `kubectl rollout pause deploy/web -n app` | Pause the deployment before a series of edits |
|         | `kubectl apply -f changes/ -n app` | Apply the batch while paused |
|         | `kubectl rollout resume deploy/web -n app` | Start rollout after accumulated changes |
| [**`kubectl kustomize\|apply -k`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#kustomize) | | **Declarative environments without Helm** |
|         | `kubectl kustomize overlays/prod` | Render the final configuration |
|         | `kubectl diff -k overlays/prod` | Diff before applying |
|         | `kubectl apply -k overlays/prod` | Apply the overlay to the target environment |
| [**`kubectl krew`**](https://krew.sigs.k8s.io/) | | **Manage kubectl plugins to extend capabilities** |
|         | `kubectl krew install df-pv` | Plugin to inspect PV usage |
|         | `kubectl krew install neat` | Plugin for “clean” YAML without managed fields |
|         | `kubectl krew list` | Show installed plugins |
| [**`kubectl apply`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply) | | **Best practice: default-deny NetworkPolicy with explicit allows** |
|         | `kubectl apply -f netpol/00-default-deny.yaml -n app` | Deny all traffic by default in `app` |
|         | `kubectl apply -f netpol/10-allow-web-to-api.yaml -n app` | Allow exactly the required directions and ports |
|         | `kubectl get netpol -n app` | Verify policies are applied |
| [**`kubectl explain`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#explain) | | **Best practice: verify SecurityContext before release** |
|         | `kubectl explain pod.spec.securityContext` | Help for pod-level securityContext fields |
|         | `kubectl explain container.securityContext` | Container-level securityContext fields |
|         | `kubectl get deploy web -n app -o yaml` | Ensure recommended fields are set in the manifest |

> ***Notes:***  
> • **Idempotency:** all steps should produce the same result on repeated runs.  
> • **Immutable images:** use digests `@sha256:…`, not floating tags.  
> • **Gates:** `diff` → `apply` → `rollout status`/`wait`—lock in order and timeouts.  
> • **Annotation triggers:** checksum of configs/secrets on the PodTemplate—explicit restarts without manual intervention.  
> • **Selectors:** a unified label scheme for environments/apps so `--prune` and queries behave predictably.  
> • **Metrics:** `kubectl top`/HPA require metrics-server; for memory/custom metrics use HPA `autoscaling/v2` in YAML.  
> • **Separation of duties:** a GitOps bot applies manifests with a single `--field-manager`, humans go via PR and diff.  
> • **Security:** least-privilege RBAC, default-deny NetworkPolicy, PDB, and resources/limits on every workload.

---

## 📦 Workloads: Deploy/STS/DS/Job/CronJob

> **Purpose:** view and troubleshoot the main workload types, create one-off and scheduled jobs, understand update strategies and pod placement.

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`kubectl get`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#get) | | **Quick overview of workloads** |
|         | `kubectl get deploy,sts,ds,job,cronjob -A` | Summary across all namespaces |
|         | `kubectl get deploy -n app -o wide` | List deployments with extra columns |
|         | `kubectl get ds -A` | One pod per node: agents, loggers, etc. |
| [**`kubectl describe deployment`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Deployment strategy and status details** |
|         | `kubectl describe deploy web -n app` | Replicas, RollingUpdate strategy, events |
|         | `kubectl get rs -n app -l app=web -o wide` | Related ReplicaSets and their parameters |
|         | `kubectl rollout status deploy/web -n app` | Track deployment rollout progress |
| [**`kubectl describe statefulset`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **Ordered pods with stable names and PVCs** |
|         | `kubectl describe sts db -n app` | Start/stop ordering, PVC template |
|         | `kubectl get pod -l statefulset.kubernetes.io/pod-name -n app` | Inspect individual STS pods |
|         | `kubectl rollout status sts/db -n app` | Wait for STS update |
| [**`kubectl describe daemonset`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#describe) | | **One pod on each eligible node** |
|         | `kubectl describe ds node-agent -A` | Target nodes, desired/available counts |
|         | `kubectl get ds node-agent -A -o wide` | Image version and node selectors |
|         | `kubectl rollout status ds/node-agent -n ops` | DaemonSet update progress |
|         | `kubectl get ds -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name \| tail -n +2 \| while read ns name; do kubectl -n "$ns" rollout status ds/"$name"; done` | Bulk across all ns (since `rollout status` lacks `-A`) |
| [**`kubectl create job`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create) | | **One-off task until completion** |
|         | `kubectl create job echo --image=alpine -- echo hi` | Simple Job with a single command |
|         | `kubectl get jobs -n app -o wide` | Check Job start/completion |
|         | `kubectl logs -n app job/echo` | Logs of pod(s) created by the Job |
| [**`kubectl create cronjob`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#create) | | **Periodic task on a schedule** |
|         | `kubectl create cronjob hello --image=busybox --schedule="*/5 * * * *" -- date` | Run every 5 minutes |
|         | `kubectl get cronjob -n app -o wide` | Overview of schedules and missed-run policy |
|         | `kubectl create job run-now --from=cronjob/hello -n app` | Trigger a one-time Job from a CronJob |
| [**`kubectl delete job`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Delete a Job and control cascading deletion of its pods** |
|         | `kubectl delete job echo -n app --cascade=foreground` | Wait for related pods to be removed |
|         | `kubectl delete job -l app=batch -n app --cascade=background` | Delete a batch of Jobs by label; pods removed in background |
|         | `kubectl delete job cleanup -n app --cascade=orphan` | Keep pods as orphans, delete the Job only |
| [**`kubectl delete cronjob`**](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#delete) | | **Delete a CronJob schedule, optionally along with created Jobs** |
|         | `kubectl delete cronjob hello -n app` | Delete the schedule only; existing Jobs remain |
|         | `kubectl delete cronjob hello -n app --cascade=foreground` | Delete the CronJob and its Jobs |
|         | `kubectl delete cronjob -l team=ops -n app` | Bulk delete CronJobs by label |

---

## 📌 YAML Mini-Templates

> **Purpose:** ready-made snippets for a quick start. Each block can be placed in a separate file (`*.yaml`) or combined with `---`, applied via `kubectl apply -f <file>`, and verified immediately.
>
> ***How to use:***
>
> 1) Save the template to a file and, if needed, add `metadata.namespace: <ns>`.
> 2) Make sure the referenced names (`Service`, `Secret`, `StorageClass`) exist or are created along with the template.
> 3) Apply: `kubectl apply -f <file.yaml>`.
> 4) Verify: `kubectl get ... -n <ns>` / `kubectl describe ... -n <ns>`.

### Deployment + Service (ClusterIP)

**What it is:** a stateless application with 2 replicas and an in-cluster Service.  
**When to use:** a basic web service that you can later attach an Ingress to.  
**Verification:**

- `kubectl get deploy,rs,pod,svc -n <ns>`
- `kubectl rollout status deploy/web -n <ns>`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels: { app: web }
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
        - name: nginx
          image: nginx:1.27.1
          ports: [ { containerPort: 80 } ]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { cpu: 500m, memory: 256Mi }
          readinessProbe:
            httpGet: { path: "/", port: 80 }
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: "/", port: 80 }
            initialDelaySeconds: 15
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector: { app: web }
  type: ClusterIP
  ports: [ { port: 80, targetPort: 80 } ]
```

### Ingress (nginx-ingress) with TLS

**What it is:** L7 HTTP(S) routing to the `web` Service.  
**Important:** requires an installed Ingress controller (e.g., ingress-nginx) and an existing TLS Secret.  
**Verification:**

- `kubectl get ingress -n <ns>`
- `kubectl describe ingress web -n <ns>`
- DNS should point to the controller’s external address

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
spec:
  ingressClassName: nginx
  tls:
    - hosts: [ "example.com" ]
      secretName: tls-example-com  # must exist (type kubernetes.io/tls)
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port: { number: 80 }
```

### PVC + using a volume in a Pod

**What it is:** a volume claim (PVC) and a Deployment that writes to this volume.  
**Important:** `storageClassName` must exist and support the required modes (RWO/RWX).  
**Verification:**

- `kubectl get pvc -n <ns>` → status Bound
- `kubectl describe pvc data -n <ns>` → binding details

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  accessModes: [ "ReadWriteOnce" ]
  storageClassName: standard
  resources: { requests: { storage: 10Gi } }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: writer }
spec:
  replicas: 1
  selector: { matchLabels: { app: writer } }
  template:
    metadata: { labels: { app: writer } }
    spec:
      containers:
        - name: app
          image: busybox
          command: ["sh","-c","while true; do date >> /data/out.txt; sleep 5; done"]
          volumeMounts: [ { name: data, mountPath: /data } ]
      volumes: [ { name: data, persistentVolumeClaim: { claimName: data } } ]
```

### HPA v2 for CPU

**What it is:** auto-scaling the web deployment based on CPU load.  
**Important:** requires metrics-server; YAML in autoscaling/v2.  
**Verification:**

- `kubectl get hpa -n <ns>`
- `kubectl describe hpa web-hpa -n <ns>`

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: web-hpa }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: web }
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 60 }
```

### NetworkPolicy: deny-all + allow from namespace web

**What it is:** full restriction of traffic in db and targeted access to the postgres pod only from ns=web on port 5432.  
**Important:** the CNI plugin must support NetworkPolicy.  
**Verification:**

- `kubectl get netpol -n db`
- Traffic from other namespaces must be blocked

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: deny-all, namespace: db }
spec:
  podSelector: {}
  policyTypes: [ Ingress, Egress ]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-from-web, namespace: db }
spec:
  podSelector: { matchLabels: { app: postgres } }
  ingress:
    - from:
        - namespaceSelector: { matchLabels: { name: web } }
      ports: [ { protocol: TCP, port: 5432 } ]
```

> ⚠️ For the namespace selector, use the actual label of your `web` namespace (for example, set it with: `kubectl label ns web name=web`).

### RBAC: read-only role in a namespace

**What it is:** a Role with read permissions on basic resources and a RoleBinding to a user.  
**Important:** the subject type (User/Group/ServiceAccount) must match your authentication.  
**Verification:**

- `kubectl auth can-i list pods -n dev --as alice@example.com`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: view-only, namespace: dev }
rules:
  - apiGroups: ["", "apps", "batch"]
    resources: ["pods", "services", "deployments", "jobs", "cronjobs"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: view-only-binding, namespace: dev }
subjects:
  - kind: User
    name: alice@example.com
    apiGroup: rbac.authorization.k8s.io
roleRef: { kind: Role, name: view-only, apiGroup: rbac.authorization.k8s.io }
```

### Debug: ephemeral container (via command)

**What it is:** adding a temporary container to an existing pod to install utilities and get a shell without changing the application image.  
**How to use:** no YAML is needed—this is a CLI operation. You need a target pod (below is a simple pod example for practice).  
**Add a debug container:**

- `kubectl debug pod/sample --image=busybox:1.36 --target=app -n <ns> -it -- sh`

**Example pod (as a debug target):**

```yaml
apiVersion: v1
kind: Pod
metadata: { name: sample }
spec:
  containers:
    - name: app
      image: ghcr.io/org/app:1.0.0
      command: ["sh","-c","sleep 3600"]
```

> ***Notes:***  
• In the templates, replace the `example.com` domain, namespace names (`<ns>`), `StorageClass`/`Secret` names, and labels with your own.  
• You can combine multiple objects in one file using `---`; apply atomically and check `rollout status` for workloads.  
• On apply errors, check `kubectl describe <obj> -n <ns>` and `kubectl get events -A --sort-by=.lastTimestamp`.

---

## 💡 kubectl Aliases

> **Purpose:** speed up day-to-day work with `kubectl` using short commands and Tab autocompletion.  
> **Where to put:** in your shell init file — **Bash:** `~/.bashrc` (or `~/.bash_profile` on macOS), **Zsh:** `~/.zshrc`. After editing, run `source ~/.bashrc` or `source ~/.zshrc`.

### Bash: autocompletion + basic set

```bash
 # --- kubectl autocompletion (must be BEFORE complete -F ...) ---
 # Load completion functions into the current session
source <(kubectl completion bash)

 # Short alias and bind completion to it
alias k=kubectl
complete -o default -F __start_kubectl k

 # --- Universal aliases (safe & frequently used) ---
 # Inventory
alias kg='kubectl get'                           # k g <resource> ...
alias kgp='kubectl get pods'                     # k g pods
alias kgpo='kubectl get pods -o wide'            # pods with extra columns
alias kgs='kubectl get svc'                      # services
alias kgi='kubectl get ingress'                  # ingress
alias kgep='kubectl get endpoints'               # endpoints
alias kgn='kubectl get nodes -o wide'            # nodes
alias kgns='kubectl get ns'                      # namespaces
alias kga='kubectl get all -A'                   # all core resources across all ns

 # Details/logs/watch
alias kdesc='kubectl describe'                   # kdesc pod/<name> -n <ns>
alias kl='kubectl logs'                          # kl pod/<name> -n <ns>
alias klf='kubectl logs -f'                      # follow logs
alias kgw='kubectl get -w'                       # watch: kgw pods -n <ns>

 # Apply/delete/rollouts
alias ka='kubectl apply -f'                      # ka manifest.yaml
alias kd='kubectl delete'                        # kd pod/<name> -n <ns>
alias kaf='kubectl apply -f'                     # explicit apply from file/dir
alias kdf='kubectl delete -f'                    # delete by file/dir
alias krr='kubectl rollout restart'              # restart a workload
alias krs='kubectl rollout status'               # rollout status

 # Access & debugging
alias ke='kubectl exec -it'                      # interactive exec
alias kpf='kubectl port-forward'                 # port forward
alias kcp='kubectl cp'                           # copy files
alias kex='kubectl explain'                      # help for API fields

 # Output formats
alias kgy='kubectl get -o yaml'                  # kgy deploy/<name> -n <ns>
alias kgj='kubectl get -o json'
alias kgnm='kubectl get -o name'

 # Quick helpers for context/namespace (handier than always typing -n/--context)
kns() { kubectl config set-context --current --namespace="${1:?usage: kns <namespace>}"; }
kctx() { kubectl config use-context "${1:?usage: kctx <context>}"; }
```

### Zsh: autocompletion + basic set

```zsh
 # --- kubectl autocompletion for Zsh ---
autoload -Uz compinit && compinit
source <(kubectl completion zsh)

 # Alias and bind completion
alias k=kubectl
compdef _kubectl k

 # Same alias set as for Bash (you can copy the blocks below)
alias kg='kubectl get'
alias kgp='kubectl get pods'
alias kgpo='kubectl get pods -o wide'
alias kgs='kubectl get svc'
alias kgi='kubectl get ingress'
alias kgep='kubectl get endpoints'
alias kgn='kubectl get nodes -o wide'
alias kgns='kubectl get ns'
alias kga='kubectl get all -A'

alias kdesc='kubectl describe'
alias kl='kubectl logs'
alias klf='kubectl logs -f'
alias kgw='kubectl get -w'

alias ka='kubectl apply -f'
alias kd='kubectl delete'
alias kaf='kubectl apply -f'
alias kdf='kubectl delete -f'
alias krr='kubectl rollout restart'
alias krs='kubectl rollout status'

alias ke='kubectl exec -it'
alias kpf='kubectl port-forward'
alias kcp='kubectl cp'
alias kex='kubectl explain'

alias kgy='kubectl get -o yaml'
alias kgj='kubectl get -o json'
alias kgnm='kubectl get -o name'

kns() { kubectl config set-context --current --namespace="${1:?usage: kns <namespace>}"; }
kctx() { kubectl config use-context "${1:?usage: kctx <context>}"; }
```

> ***Notes:***  
> • Load **completion** first, then declare `alias k=kubectl` and bind completion (`complete ...` or `compdef`).  
> • The `kns/kctx` functions change the current values in `kubeconfig` — safer than a forgotten `-n` in prod.  
> • Avoid “aggressive” aliases like unconditional `delete -A` — they’re dangerous on large clusters.  
> • If you use `kubectx/kubens`, you can replace the `kctx/kns` functions with those utilities.  
> • For a persistent “watcher” you can define `kw() { watch -n 1 kubectl "$@"; }` (the `watch` package is required separately).

---

## 📚 Additional resources

> **Purpose**: quick links to official references and vetted tools to dive exactly where needed — networking, storage, security, autoscaling, GitOps, local clusters.

### 💡 Tips

- Choose the documentation version that matches your cluster (version selector in the top-right of the docs).  
- Check client/server compatibility: `kubectl` ↔ API server (Version Skew).  
- For Ingress/CNI/CSI always read the docs of the **specific** controller/driver — annotations and behavior differ.  
- Looking for a precise field/type? Use the **Kubernetes API Reference** + `kubectl explain <kind>.<path>`.  
- For step-by-step actions — the **Tasks** section; for theory — **Concepts**.  
- Avoid outdated posts (especially about flags/annotations) — aim for ≤ 12–18 months.  
- Within your team, pin links to a **specific minor version** of the docs to avoid drift.

### 🌐 Useful links

#### 📘 Official references

| Resource | Description |
| ------ | -------- |
| [Kubernetes Documentation](https://kubernetes.io/docs/home/) | Main Kubernetes docs: concepts, guides, tasks |
| [kubectl Reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/) | Full list of `kubectl` commands |
| [Kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) | Official `kubectl` cheat sheet |
| [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/) | Complete API object reference |
| [Version Skew Policy](https://kubernetes.io/docs/setup/release/version-skew-policy/) | Client/server and component version compatibility |

#### 📙 Networking

| Resource | Description |
| ------ | -------- |
| [Services](https://kubernetes.io/docs/concepts/services-networking/service/) | Service types and port exposure |
| [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) | L7 routing to services |
| [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) | L3/L4 policies and application |

#### 📗 Scaling and metrics

| Resource | Description |
| ------ | -------- |
| [HPA v2](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) | Autoscaling by CPU/memory/custom metrics |
| [metrics-server](https://github.com/kubernetes-sigs/metrics-server) | Metrics source for `kubectl top` and HPA |

#### 📕 Storage

| Resource | Description |
| ------ | -------- |
| [Persistent Volumes (PV/PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) | Reclaim policies, binding |
| [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/) | Dynamic provisioning |
| [CSI Drivers (catalog)](https://kubernetes-csi.github.io/docs/drivers.html) | List of CSI drivers |

#### 📘 Security and access

| Resource | Description |
| ------ | -------- |
| [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) | Baseline pod security profiles |
| [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) | Roles, bindings, permissions |
| [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) | Secret types and usage |
| [Ephemeral Containers / `kubectl debug`](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container) | Debugging without changing the image |

#### 📙 Workloads and core objects

| Resource | Description |
| ------ | -------- |
| [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) | Stateless applications and rollouts |
| [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) | Stable identity/volumes |
| [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) | One pod per node |
| [Jobs/CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) | Batch and scheduled jobs |
| [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) | Application configuration |

#### 📗 Local clusters

| Resource | Description |
| ------ | -------- |
| [kind](https://kind.sigs.k8s.io/) | Kubernetes in Docker for CI/local development |
| [minikube](https://minikube.sigs.k8s.io/docs/) | Single-node local cluster |

#### 📕 `kubectl` plugins

| Resource | Description |
| ------ | -------- |
| [Krew](https://krew.sigs.k8s.io/) | Plugin manager for `kubectl` |
| [kubectl-neat](https://github.com/itaysk/kubectl-neat) | “Clean” YAML without boilerplate fields |
| [kubectx / kubens](https://github.com/ahmetb/kubectx) | Fast context and namespace switching |
