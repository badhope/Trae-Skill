---
name: e2e-test
description: "End-to-end testing for complete user flows. Supports Playwright, Cypress, Selenium. Keywords: e2e test, playwright, cypress, selenium, 端到端测试"
layer: domain
role: specialist
version: 2.0.0
domain: testing
languages:
  - javascript
  - typescript
  - python
frameworks:
  - playwright
  - cypress
  - selenium
  - puppeteer
invoked_by:
  - coding-workflow
  - test-generator
capabilities:
  - browser_automation
  - user_flow_testing
  - visual_regression
  - cross_browser_testing
  - mobile_testing
---

# E2E Test

端到端测试专家，专注于完整用户流程的自动化测试，模拟真实用户行为。

## 适用场景

- 用户注册登录流程
- 购物车和结账流程
- 表单提交和验证
- 多页面交互
- 跨浏览器兼容性

## 框架指南

### 1. Playwright (推荐)

```typescript
import { test, expect, Page, BrowserContext } from '@playwright/test';

test.describe('User Authentication Flow', () => {
  let context: BrowserContext;
  let page: Page;
  
  test.beforeAll(async ({ browser }) => {
    context = await browser.newContext();
    page = await context.newPage();
  });
  
  test.afterAll(async () => {
    await context.close();
  });
  
  test('should complete registration flow', async () => {
    await page.goto('/register');
    
    await page.fill('[name="name"]', 'John Doe');
    await page.fill('[name="email"]', 'john@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="confirmPassword"]', 'SecurePass123!');
    
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL(/\/dashboard/);
    await expect(page.locator('.welcome-message')).toContainText('Welcome, John');
  });
  
  test('should show validation errors', async () => {
    await page.goto('/register');
    
    await page.click('button[type="submit"]');
    
    await expect(page.locator('.error-message')).toContainText('Name is required');
    await expect(page.locator('.error-message')).toContainText('Email is required');
  });
  
  test('should login and access protected content', async () => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL(/\/dashboard/);
    
    await page.click('[data-testid="profile-menu"]');
    await page.click('text=My Profile');
    
    await expect(page.locator('.profile-email')).toHaveText('test@example.com');
  });
});

test.describe('Shopping Cart Flow', () => {
  test.use({ storageState: 'auth.json' });
  
  test('should add item to cart and checkout', async ({ page }) => {
    await page.goto('/products');
    
    await page.click('[data-testid="product-1"] >> text=Add to Cart');
    
    await expect(page.locator('.cart-count')).toHaveText('1');
    
    await page.click('[data-testid="cart-icon"]');
    
    await expect(page.locator('.cart-item')).toHaveCount(1);
    await expect(page.locator('.cart-total')).toContainText('$99.99');
    
    await page.click('text=Proceed to Checkout');
    
    await page.fill('[name="cardNumber"]', '4242424242424242');
    await page.fill('[name="expiry"]', '12/25');
    await page.fill('[name="cvv"]', '123');
    
    await page.click('button:has-text("Place Order")');
    
    await expect(page).toHaveURL(/\/order-confirmation/);
    await expect(page.locator('.order-number')).toBeVisible();
  });
  
  test('should handle out of stock items', async ({ page }) => {
    await page.goto('/products/out-of-stock-item');
    
    await expect(page.locator('button:has-text("Add to Cart")')).toBeDisabled();
    await expect(page.locator('.stock-status')).toHaveText('Out of Stock');
  });
});

test.describe('Visual Regression', () => {
  test('homepage should match snapshot', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });
  
  test('product card should match snapshot', async ({ page }) => {
    await page.goto('/products/1');
    const card = page.locator('.product-card');
    await expect(card).toHaveScreenshot('product-card.png');
  });
});

test.describe('Mobile Responsive', () => {
  test.use({ viewport: { width: 375, height: 667 } });
  
  test('should show mobile menu', async ({ page }) => {
    await page.goto('/');
    
    await page.click('[data-testid="mobile-menu-toggle"]');
    
    await expect(page.locator('.mobile-menu')).toBeVisible();
    await expect(page.locator('.mobile-menu a')).toHaveCount(5);
  });
});

test.describe('Accessibility', () => {
  test('should have no accessibility violations', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });
});

test.describe('API Mocking', () => {
  test('should handle API error gracefully', async ({ page }) => {
    await page.route('**/api/products', route => {
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: 'Server error' })
      });
    });
    
    await page.goto('/products');
    
    await expect(page.locator('.error-message')).toContainText('Failed to load products');
    await expect(page.locator('button:has-text("Retry")')).toBeVisible();
  });
  
  test('should mock successful API response', async ({ page }) => {
    await page.route('**/api/users/me', route => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({
          id: '1',
          name: 'Mocked User',
          email: 'mocked@example.com'
        })
      });
    });
    
    await page.goto('/dashboard');
    
    await expect(page.locator('.user-name')).toHaveText('Mocked User');
  });
});
```

### 2. Cypress

```javascript
describe('User Authentication', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  
  it('should register a new user', () => {
    cy.get('[data-testid="register-link"]').click();
    
    cy.get('[name="name"]').type('John Doe');
    cy.get('[name="email"]').type('john@example.com');
    cy.get('[name="password"]').type('SecurePass123!');
    cy.get('[name="confirmPassword"]').type('SecurePass123!');
    
    cy.get('button[type="submit"]').click();
    
    cy.url().should('include', '/dashboard');
    cy.get('.welcome-message').should('contain', 'Welcome, John');
    
    cy.getCookie('auth_token').should('exist');
  });
  
  it('should show validation errors', () => {
    cy.get('[data-testid="register-link"]').click();
    cy.get('button[type="submit"]').click();
    
    cy.get('.error-message').should('contain', 'Name is required');
    cy.get('.error-message').should('contain', 'Email is required');
  });
  
  it('should login with valid credentials', () => {
    cy.get('[data-testid="login-link"]').click();
    
    cy.get('[name="email"]').type('test@example.com');
    cy.get('[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    
    cy.url().should('include', '/dashboard');
  });
});

describe('Shopping Cart', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password123');
  });
  
  it('should add item to cart', () => {
    cy.visit('/products');
    
    cy.get('[data-testid="product-1"]').within(() => {
      cy.get('button:contains("Add to Cart")').click();
    });
    
    cy.get('.cart-count').should('have.text', '1');
    
    cy.get('[data-testid="cart-icon"]').click();
    
    cy.get('.cart-item').should('have.length', 1);
    cy.get('.cart-total').should('contain', '$99.99');
  });
  
  it('should complete checkout', () => {
    cy.addProductToCart(1);
    cy.visit('/cart');
    
    cy.get('button:contains("Checkout")').click();
    
    cy.get('[name="cardNumber"]').type('4242424242424242');
    cy.get('[name="expiry"]').type('1225');
    cy.get('[name="cvv"]').type('123');
    
    cy.get('button:contains("Place Order")').click();
    
    cy.url().should('include', '/order-confirmation');
    cy.get('.order-number').should('be.visible');
  });
});

describe('API Interception', () => {
  it('should handle API error', () => {
    cy.intercept('GET', '/api/products', {
      statusCode: 500,
      body: { error: 'Server error' }
    });
    
    cy.visit('/products');
    
    cy.get('.error-message').should('contain', 'Failed to load products');
  });
  
  it('should wait for API response', () => {
    cy.intercept('GET', '/api/products').as('getProducts');
    
    cy.visit('/products');
    
    cy.wait('@getProducts').its('response.statusCode').should('eq', 200);
    
    cy.get('.product-list').should('be.visible');
  });
});

Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[name="email"]').type(email);
    cy.get('[name="password"]').type(password);
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});

Cypress.Commands.add('addProductToCart', (productId) => {
  cy.visit('/products');
  cy.get(`[data-testid="product-${productId}"] button:contains("Add to Cart")`).click();
});
```

### 3. Selenium (Python)

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

class TestUserAuthentication:
    def test_register_new_user(self, driver):
        driver.get("https://example.com/register")
        
        driver.find_element(By.NAME, "name").send_keys("John Doe")
        driver.find_element(By.NAME, "email").send_keys("john@example.com")
        driver.find_element(By.NAME, "password").send_keys("SecurePass123!")
        driver.find_element(By.NAME, "confirmPassword").send_keys("SecurePass123!")
        
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("/dashboard")
        )
        
        welcome = driver.find_element(By.CLASS_NAME, "welcome-message")
        assert "Welcome, John" in welcome.text
    
    def test_login_flow(self, driver):
        driver.get("https://example.com/login")
        
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("/dashboard")
        )
        
        assert "dashboard" in driver.current_url

class TestShoppingCart:
    def test_add_to_cart(self, driver):
        driver.get("https://example.com/products")
        
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='product-1'] button"))
        )
        add_button.click()
        
        cart_count = driver.find_element(By.CLASS_NAME, "cart-count")
        assert cart_count.text == "1"
    
    def test_checkout_flow(self, driver):
        driver.get("https://example.com/cart")
        
        driver.find_element(By.NAME, "cardNumber").send_keys("4242424242424242")
        driver.find_element(By.NAME, "expiry").send_keys("1225")
        driver.find_element(By.NAME, "cvv").send_keys("123")
        
        driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]").click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("/order-confirmation")
        )
        
        order_number = driver.find_element(By.CLASS_NAME, "order-number")
        assert order_number.is_displayed()
```

## 测试模式

### Page Object Model

```typescript
class LoginPage {
  constructor(private page: Page) {}
  
  async navigate() {
    await this.page.goto('/login');
  }
  
  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email);
    await this.page.fill('[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }
  
  async getErrorMessage() {
    return this.page.locator('.error-message').textContent();
  }
}

test('should login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await loginPage.login('test@example.com', 'password123');
  await expect(page).toHaveURL(/\/dashboard/);
});
```

## 最佳实践

1. **稳定性优先**: 避免脆弱的选择器
2. **等待策略**: 使用智能等待而非固定等待
3. **数据隔离**: 每个测试独立数据
4. **并行执行**: 提高测试效率
5. **视觉回归**: 捕获UI变化
6. **跨浏览器**: 覆盖主流浏览器
7. **移动端测试**: 响应式验证

## 相关技能

- [unit-test](../unit-test) - 单元测试
- [integration-test](../integration-test) - 集成测试
- [frontend-react](../frontend/react) - React开发
- [frontend-vue](../frontend/vue) - Vue开发
