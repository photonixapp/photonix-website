# Testing

Photonix has two types of tests: Python backend tests (pytest) and frontend end-to-end tests (Playwright).

## Backend Tests (Python/pytest)

We have Python tests to cover most of the the server-side logic. We use pytest as a test runner and recommend running the tests inside the Docker container.

If you have the code checked out and can run Makefiles then you can start the container if it isn't already running:

    make start

If you can't run the Makefile directly (e.g. if you're on Windows) then you can see what the equivalent command would be by looking inside that file. The command for starting the environment with out make is:

    docker compose -f docker/docker-compose.dev.yml up

In another teminal connect to the Photonix Docker container and execute the test runner:

    make shell
    python test.py

To start the shell without make would be:

    docker compose -f docker/docker-compose.dev.yml exec photonix bash

If you are only interested in a particular test and want to save time you can add the test file path as an extra argument, i.e:

    python test.py tests/test_metadata.py

If you are familiar with pytest then you can add extra arguments to the end and they will be passed through.

If you are an expert with pytest and have suggestions for improving this setup then please do get in touch with your suggestions.

## Frontend Tests (Playwright)

We use Playwright for end-to-end testing of the React frontend. These tests run against the actual application in Docker containers and test real user flows.

### Prerequisites

Make sure the development environment is running:

    make start

Then install Playwright dependencies in the `ui` directory:

    cd ui
    npm install
    npx playwright install

### Running Tests

Run all Playwright tests:

    cd ui
    npx playwright test

Run a specific test file:

    npx playwright test e2e/auth.spec.ts

Run tests in headed mode (see the browser):

    npx playwright test --headed

Run tests with UI mode for debugging:

    npx playwright test --ui

### Test Configuration

Tests are configured to run serially (one at a time) because they share the same database. This is set in `ui/playwright.config.ts`.

### Test Data Setup

Playwright tests create their own test data using Django management commands executed via Docker. The shared test utilities in `ui/e2e/test-utils.ts` provide helpers for:

- **`setupTestUser(username, password)`** - Creates a test user with a fully configured library (required to bypass onboarding redirects)
- **`cleanupTestUser(username)`** - Removes the test user and all associated data (library, library paths, etc.)
- **`login(page, username, password)`** - Logs in with the specified credentials
- **`createTestPhotos(username, count, options)`** - Creates test photos (solid colour images, optionally tagged) in the user's library
- **`cleanupTestPhotos(username)`** - Removes the test photos and tags
- **`runDjangoCommand(pythonCode)`** - Executes arbitrary Python code in the Django shell via Docker

Example usage in a test:

```typescript
import { setupTestUser, cleanupTestUser, login } from './test-utils'

test.beforeAll(async () => {
  setupTestUser('myuser', 'mypassword')
})

test.afterAll(async () => {
  cleanupTestUser('myuser')
})

test('my test', async ({ page }) => {
  await login(page, 'myuser', 'mypassword')
  // ... test assertions
})
```

### Viewing Test Reports

After running tests, Playwright generates an HTML report. To view it:

    npx playwright show-report

This opens a browser with detailed results including:

- Pass/fail status for each test
- Test duration
- Screenshots and traces for failed tests
- Error messages and stack traces

### Test Structure

The test files are located in `ui/e2e/`:

- `auth.spec.ts` - Authentication flows (login, logout, session persistence)
- `onboarding.spec.ts` - New user onboarding wizard
- `library-switching.spec.ts` - Library selection and switching
- `invite.spec.ts` - Adding users to libraries and invitation links
- `settings.spec.ts` - Settings area (password and profile changes)
- `thumbnails.spec.ts` - Thumbnail grid and selection
- `search.spec.ts` - Search bar, autocomplete and filters
- `photo-detail.spec.ts` - Photo detail view and keyboard navigation
- `bounding-boxes.spec.ts` - Object bounding boxes on the photo detail view
- `image-resolution.spec.ts` - Image resolution chosen for viewport size and pixel density
- `tile-zoom.spec.ts` - Tiled zooming of large images

### Debugging Failed Tests

When a test fails, Playwright captures useful debugging information:

1. **Screenshots** - Automatically captured at the point of failure
2. **Traces** - Recorded on first retry (configurable in `playwright.config.ts`)
3. **Error context** - Saved in `test-results/` directory

To view a trace file:

    npx playwright show-trace test-results/path-to-trace.zip

For interactive debugging, use the `--debug` flag:

    npx playwright test --debug
