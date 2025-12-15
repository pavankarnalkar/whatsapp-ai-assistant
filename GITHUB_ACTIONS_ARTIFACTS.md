# GitHub Actions Artifacts - File Upload Location

## Where Are Files Uploaded?

When you use `actions/upload-artifact` in a GitHub Actions workflow, files are uploaded to **GitHub's artifact storage system**, not to your repository.

## Accessing Uploaded Artifacts

### Method 1: Via GitHub Web Interface

1. Go to your repository on GitHub: `https://github.com/{owner}/{repo}`
2. Click on the **"Actions"** tab
3. Select the workflow run you're interested in
4. Scroll to the bottom of the page
5. Look for the **"Artifacts"** section
6. Click on the artifact name to download it

### Method 2: Via Direct URL

Artifacts can be accessed at:
```
https://github.com/{owner}/{repo}/actions/runs/{run_id}
```

Replace:
- `{owner}` - Repository owner (username or organization)
- `{repo}` - Repository name
- `{run_id}` - Specific workflow run ID (visible in the URL when viewing a workflow run)

### Method 3: Via GitHub CLI

```bash
# List artifacts for a workflow run
gh run view {run_id} --repo {owner}/{repo}

# Download an artifact
gh run download {run_id} --name {artifact-name} --repo {owner}/{repo}
```

### Method 4: Via GitHub API

```bash
# List artifacts for a repository
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/{owner}/{repo}/actions/artifacts

# Download a specific artifact
curl -L -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/{owner}/{repo}/actions/artifacts/{artifact_id}/zip \
  -o artifact.zip
```

## Storage Details

### Default Settings
- **Retention Period**: 90 days (configurable in workflow)
- **Storage Location**: GitHub's cloud infrastructure (not in your repo)
- **Maximum Size**: 10 GB per artifact
- **Total Storage**: Limited by your GitHub plan

### Retention Configuration

You can customize retention in your workflow:

```yaml
- name: Upload artifacts
  uses: actions/upload-artifact@v4
  with:
    name: my-artifact
    path: path/to/files/
    retention-days: 30  # Keep for 30 days (1-90 days)
```

### Repository Settings

Default retention can be configured at the repository level:
1. Repository Settings → Actions → General
2. Scroll to "Artifact and log retention"
3. Set default retention period (1-90 days, with higher limits available for enterprise accounts)

## Important Notes

1. **Not in Repository**: Artifacts are NOT committed to your repository. They're stored separately in GitHub's artifact storage.

2. **Temporary Storage**: Artifacts are automatically deleted after the retention period expires.

3. **No Version Control**: Artifacts are not version-controlled. They're simply file storage.

4. **Download Only**: You can only download entire artifacts, not browse individual files in the UI.

5. **Billing**: Artifact storage and transfer may count against your GitHub Actions minutes/storage limits, depending on your plan.

## Example Workflow

```yaml
name: Build and Upload

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build project
        run: |
          mkdir -p dist
          echo "Build output" > dist/output.txt
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-results
          path: dist/
          retention-days: 30
```

## Finding Artifacts for Your Repository

Artifacts from CI runs can be found at:

```
https://github.com/{owner}/{repo}/actions
```

Replace `{owner}` with the repository owner and `{repo}` with the repository name.

Select any workflow run, and scroll to the bottom to see available artifacts.

## Common Issues

### "No artifacts found"
- Check if the workflow step completed successfully
- Verify the path in `upload-artifact` exists and contains files
- Check workflow run logs for upload errors

### "Artifact expired"
- Artifacts have a limited retention period
- Re-run the workflow to generate new artifacts

### "Cannot download artifact"
- Ensure you have read access to the repository
- Artifacts are only available for completed workflow runs
- Check if the retention period has expired

## References

- [GitHub Actions Artifacts Documentation](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)
- [actions/upload-artifact](https://github.com/actions/upload-artifact)
- [actions/download-artifact](https://github.com/actions/download-artifact)
