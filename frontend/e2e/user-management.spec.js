import { expect, test } from '@playwright/test';

const API_BASE = 'http://127.0.0.1:8000';

const seedUsers = [
  {
    id: 1,
    first_name: 'Grace',
    last_name: 'Hopper',
    username: 'grace.hopper',
    phone_number: '+1 555 0101',
    address: 'Arlington, VA',
  },
  {
    id: 2,
    first_name: 'Ada',
    last_name: 'Lovelace',
    username: 'ada.lovelace',
    phone_number: '+44 20 7946 0000',
    address: 'London, UK',
  },
  {
    id: 3,
    first_name: 'Linus',
    last_name: 'Torvalds',
    username: 'linus.torvalds',
    phone_number: '+358 555 0103',
    address: 'Helsinki, Finland',
  },
];

function userMatchesSearch(user, searchTerm) {
  const normalizedTerm = searchTerm.toLowerCase();
  return [
    user.first_name,
    user.last_name,
    user.username,
    user.phone_number,
    user.address,
  ].some((value) => value?.toLowerCase().includes(normalizedTerm));
}

function sortUsers(users, sortBy, sortOrder) {
  if (!sortBy) return [...users];

  return [...users].sort((a, b) => {
    const first = String(a[sortBy] ?? '').toLowerCase();
    const second = String(b[sortBy] ?? '').toLowerCase();
    const result = first.localeCompare(second);
    return sortOrder === 'desc' ? -result : result;
  });
}

async function mockUsersApi(page, initialUsers = seedUsers) {
  let users = initialUsers.map((user) => ({ ...user }));
  let nextId = Math.max(...users.map((user) => user.id), 0) + 1;

  await page.route(`${API_BASE}/users**`, async (route) => {
    const request = route.request();
    const url = new URL(request.url());
    const method = request.method();

    if (method === 'GET' && url.pathname === '/users/suggest-username') {
      const firstName = url.searchParams.get('first_name') ?? '';
      const lastName = url.searchParams.get('last_name') ?? '';
      const baseUsername = `${firstName}.${lastName}`.toLowerCase().replace(/\s/g, '');
      let username = baseUsername;
      let suffix = 1;

      while (users.some((user) => user.username === username)) {
        username = `${baseUsername}${suffix}`;
        suffix += 1;
      }

      await route.fulfill({ json: { username } });
      return;
    }

    if (method === 'GET' && url.pathname === '/users') {
      const skip = Number(url.searchParams.get('skip') ?? 0);
      const limit = Number(url.searchParams.get('limit') ?? 10);
      const search = url.searchParams.get('search');
      const sortBy = url.searchParams.get('sort_by');
      const sortOrder = url.searchParams.get('sort_order') ?? 'asc';

      let result = users;
      if (search) {
        result = result.filter((user) => userMatchesSearch(user, search));
      }

      result = sortUsers(result, sortBy, sortOrder);

      await route.fulfill({
        json: {
          users: result.slice(skip, skip + limit),
          total_count: result.length,
        },
      });
      return;
    }

    if (method === 'POST' && url.pathname === '/users/') {
      const payload = await request.postDataJSON();

      if (users.some((user) => user.username === payload.username)) {
        await route.fulfill({
          status: 400,
          json: { detail: 'Username already exists' },
        });
        return;
      }

      const createdUser = { id: nextId, ...payload };
      nextId += 1;
      users = [createdUser, ...users];

      await route.fulfill({ status: 201, json: createdUser });
      return;
    }

    const userPathMatch = url.pathname.match(/^\/users\/(\d+)$/);
    if (userPathMatch) {
      const userId = Number(userPathMatch[1]);
      const existingUser = users.find((user) => user.id === userId);

      if (!existingUser) {
        await route.fulfill({ status: 404, json: { detail: 'User not found' } });
        return;
      }

      if (method === 'PUT') {
        const payload = await request.postDataJSON();
        const updatedUser = { ...existingUser, ...payload, id: userId };
        users = users.map((user) => (user.id === userId ? updatedUser : user));
        await route.fulfill({ json: updatedUser });
        return;
      }

      if (method === 'DELETE') {
        users = users.filter((user) => user.id !== userId);
        await route.fulfill({ json: { detail: 'User deleted' } });
        return;
      }
    }

    await route.fulfill({ status: 404, json: { detail: 'Unhandled test route' } });
  });
}

test.beforeEach(async ({ page }) => {
  await mockUsersApi(page);
});

test('lists users and supports search, sorting, and empty results', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveURL(/\/dashboard$/);
  await expect(page.getByRole('heading', { name: 'User Administration' })).toBeVisible();
  await expect(page.getByRole('table', { name: 'Users table' })).toContainText('Grace');
  await expect(page.getByText('3 total users')).toBeVisible();

  await page.getByLabel('Search users by name, username, phone or address').fill('hopper');
  await expect(page.getByText('1 total user')).toBeVisible();
  await expect(page.getByRole('cell', { name: 'Grace', exact: true })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'Ada', exact: true })).toBeHidden();

  await page.getByRole('button', { name: 'Clear search', exact: true }).click();
  await expect(page.getByText('3 total users')).toBeVisible();

  await page.getByRole('columnheader', { name: /First Name/ }).click();
  await expect(page.locator('tbody tr').first()).toContainText('Ada');

  await page.getByRole('columnheader', { name: /First Name/ }).click();
  await expect(page.locator('tbody tr').first()).toContainText('Linus');

  await page.getByLabel('Search users by name, username, phone or address').fill('no-match');
  await expect(page.getByText('No results found matching "no-match"')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Clear Search', exact: true })).toBeVisible();
});

test('creates, edits, and deletes a user', async ({ page }) => {
  await page.goto('/dashboard');

  await page.getByRole('button', { name: 'Add new user' }).click();
  const createDialog = page.getByRole('dialog', { name: 'Create New User' });
  await expect(createDialog).toBeVisible();

  await createDialog.getByLabel('First Name').fill('Mina');
  await createDialog.getByLabel('Last Name').fill('Stone');
  await expect(createDialog.getByLabel('Username')).toHaveValue('mina.stone');
  await createDialog.getByLabel('Telephone Number').fill('+1 555 0199');
  await createDialog.getByLabel('Address').fill('New York, NY');
  await createDialog.getByRole('button', { name: 'Create new user' }).click();

  await expect(page.getByRole('alert').filter({ hasText: 'User created successfully!' })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'Mina', exact: true })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'Stone', exact: true })).toBeVisible();

  await page.getByRole('button', { name: 'Edit user Mina Stone' }).click();
  const editDialog = page.getByRole('dialog', { name: 'Edit User' });
  await expect(editDialog).toBeVisible();

  await editDialog.getByLabel('Last Name').fill('Starr');
  await editDialog.getByRole('button', { name: 'Save user changes' }).click();

  await expect(page.getByRole('alert').filter({ hasText: 'User updated successfully!' })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'Starr', exact: true })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'Stone', exact: true })).toBeHidden();

  await page.getByRole('button', { name: 'Delete user Mina Starr' }).click();
  const deleteDialog = page.getByRole('dialog', { name: 'Confirm Deletion' });
  await expect(deleteDialog).toContainText('Mina Starr');
  await deleteDialog.getByRole('button', { name: 'Confirm permanent deletion' }).click();

  await expect(page.getByRole('alert').filter({ hasText: 'User deleted successfully!' })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'Mina', exact: true })).toBeHidden();
});

test('validates create form input and shows API errors', async ({ page }) => {
  await page.goto('/dashboard');

  await page.getByRole('button', { name: 'Add new user' }).click();
  const dialog = page.getByRole('dialog', { name: 'Create New User' });
  const submitButton = dialog.getByRole('button', { name: 'Create new user' });

  await expect(submitButton).toBeDisabled();

  await dialog.getByLabel('First Name').fill('Test');
  await dialog.getByLabel('Last Name').fill('User');
  await dialog.getByLabel('Username').fill('ada.lovelace');
  await dialog.getByLabel('Telephone Number').fill('bad');

  await expect(dialog.getByText('Invalid format')).toBeVisible();
  await expect(submitButton).toBeDisabled();

  await dialog.getByLabel('Telephone Number').fill('+1 555 0111');
  await expect(submitButton).toBeEnabled();
  await submitButton.click();

  await expect(dialog.getByRole('alert')).toContainText('Username already exists');
});

test('renders the not found page and returns to the dashboard', async ({ page }) => {
  await page.goto('/missing-page');

  await expect(page.getByRole('heading', { name: '404' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Page Not Found' })).toBeVisible();

  await page.getByRole('button', { name: 'Go to Dashboard' }).click();

  await expect(page).toHaveURL(/\/dashboard$/);
  await expect(page.getByRole('heading', { name: 'User Administration' })).toBeVisible();
});
