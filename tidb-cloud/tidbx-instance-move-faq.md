# TiDB X Project and Dedicated Project: what changed and why instances need to move

## What changed

TiDB Cloud introduces **typed projects** to provide a clearer separation between different product tiers. Projects are classified into two distinct types:

- **TiDB X Project** — designed for TiDB Cloud X instances (Starter, Essential, Premium)
- **Dedicated Project** — designed for TiDB Cloud Dedicated clusters

Each project type can **only host its own resource type**:

- A TiDB X Project can only contain TiDB X instances.
- A Dedicated Project can only contain Dedicated clusters.

This typed project model maintains a consistent **Organization → Project → Resource** hierarchy across all tiers, while allowing each product line to evolve with its own project behavior and capabilities.

## Why two project types

TiDB X Projects and Dedicated Projects serve different use cases and have different characteristics:

| Capability | TiDB X Project | Dedicated Project |
|---|---|---|
| Project Settings | ❌ | ✅ |
| Project-level RBAC | ✅ | ✅ |
| Billing Aggregation | ✅ | ✅ |
| Move instances between projects | ✅ | ❌ |
| Project is optional | ✅ (instances can exist at the organization level) | ❌ (clusters must belong to a project) |
| Resource type | TiDB X instances only | Dedicated clusters only |

### TiDB X Project

- **Lightweight and optional**. You can create TiDB X instances without assigning them to a project. Projects are useful when you want to organize and group resources, but they are not required.
- **Instance mobility**. You can move TiDB X instances between TiDB X Projects or back to the organization level, giving you flexibility in how you organize your resources.

### Dedicated Project

- **Mandatory project membership**. Every Dedicated cluster must belong to a Dedicated Project.
- **No instance mobility across projects**. Dedicated clusters cannot be moved between projects due to their infrastructure bindings.

## Why instances need to move

Before this change, a single project could contain both Dedicated clusters and TiDB X instances (Starter, Essential). With the introduction of typed projects, this mixed state is no longer supported.

**If your Dedicated Project currently contains TiDB X instances (Starter or Essential), you need to move those instances out.**

This is because:

1. **Each project type now exclusively hosts its own resource type.** A Dedicated Project can only contain Dedicated clusters, and a TiDB X Project can only contain TiDB X instances.
2. **TiDB X instances and Dedicated clusters have different project behaviors.** TiDB X instances benefit from lightweight, optional project membership and instance mobility — capabilities that do not apply within a Dedicated Project.
3. **Keeping them separated ensures a consistent experience.** When you interact with a Dedicated Project, you expect Dedicated-specific settings and behaviors. Mixing resource types would create confusion around which capabilities apply.

## What happens when you move instances

When you move TiDB X instances out of a Dedicated Project:

- TiDB Cloud moves the instances to a **TiDB X Project**.
- No data or service disruption occurs. This is a resource re-organization action, not an infrastructure change.
- After the move, you manage your TiDB X instances through TiDB X Projects (or at the organization level), and you continue to manage your Dedicated clusters through Dedicated Projects.

## Summary

| Before | After |
|---|---|
| A single project could contain both Dedicated clusters and TiDB X instances | Each project type exclusively hosts its own resource type |
| TiDB X instances in Dedicated Projects inherited Dedicated project behaviors | TiDB X instances are managed in TiDB X Projects with their own lightweight model |
| No distinction between project types | Clear separation: TiDB X Project vs Dedicated Project |

This change gives each product tier a project model that fits its own needs, while keeping the overall organization structure consistent and predictable.
