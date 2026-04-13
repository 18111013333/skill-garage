## Resource Leaks

- Dangling images grow unbounded — `docker image prune` regularly
- Build cache grows forever — `docker builder prune` reclaims space
- Stopped containers consume disk — `docker container prune` or `--rm` on run
- Networks pile up from compose projects — `docker network prune`

## Secrets and Security

- ENV and COPY bake secrets into layer history permanently — use secrets mount or runtime env
- `--privileged` disables all security — almost never needed, find specific capability instead
- Images from unknown registries may be malicious — verify sources
- Build args visible in image history — don't use for secrets

## Debugging

- Exit code 137 = OOM killed, 139 = segfault — check `docker inspect --format='{{.State.ExitCode}}'`
- Container won't start: check logs even for failed containers — `docker logs <container>`
- No shell in distroless images — `docker cp` files out or use debug sidecar
- Inspect filesystem of dead container — `docker cp deadcontainer:/path ./local`

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `devops` — deployment pipelines
- `linux` — host system management
- `server` — server administration

## Feedback

- If useful: `clawhub star docker`
- Stay updated: `clawhub sync`
