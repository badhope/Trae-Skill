---
name: unit-test
description: "Unit testing specialist for isolated component testing. Supports Jest, pytest, Go test, JUnit. Keywords: unit test, jest, pytest, unittest, 单元测试"
layer: domain
role: specialist
version: 2.0.0
domain: testing
languages:
  - javascript
  - typescript
  - python
  - go
  - java
frameworks:
  - jest
  - pytest
  - unittest
  - go test
  - junit
invoked_by:
  - coding-workflow
  - test-generator
capabilities:
  - test_case_design
  - mock_stub_creation
  - assertion_patterns
  - test_coverage_analysis
  - isolated_testing
---

# Unit Test

单元测试专家，专注于隔离组件的独立测试，确保每个函数和模块的正确性。

## 适用场景

- 函数和方法测试
- 类和模块测试
- 纯逻辑验证
- 边界条件测试
- 回归测试

## 框架指南

### 1. Jest (JavaScript/TypeScript)

```javascript
describe('UserService', () => {
  let userService;
  let mockRepository;
  
  beforeEach(() => {
    mockRepository = {
      findById: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn()
    };
    userService = new UserService(mockRepository);
  });
  
  afterEach(() => {
    jest.clearAllMocks();
  });
  
  describe('getUserById', () => {
    it('should return user when found', async () => {
      const mockUser = { id: '1', name: 'John', email: 'john@example.com' };
      mockRepository.findById.mockResolvedValue(mockUser);
      
      const result = await userService.getUserById('1');
      
      expect(result).toEqual(mockUser);
      expect(mockRepository.findById).toHaveBeenCalledWith('1');
    });
    
    it('should throw NotFoundError when user not found', async () => {
      mockRepository.findById.mockResolvedValue(null);
      
      await expect(userService.getUserById('999'))
        .rejects.toThrow(NotFoundError);
    });
    
    it('should throw ValidationError for invalid id', async () => {
      await expect(userService.getUserById(''))
        .rejects.toThrow(ValidationError);
      
      expect(mockRepository.findById).not.toHaveBeenCalled();
    });
  });
  
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      const input = { name: 'John', email: 'john@example.com' };
      const created = { id: '1', ...input };
      mockRepository.create.mockResolvedValue(created);
      
      const result = await userService.createUser(input);
      
      expect(result).toEqual(created);
      expect(mockRepository.create).toHaveBeenCalledWith(input);
    });
    
    it('should throw ValidationError for duplicate email', async () => {
      const input = { name: 'John', email: 'existing@example.com' };
      mockRepository.create.mockRejectedValue(new DuplicateError('Email exists'));
      
      await expect(userService.createUser(input))
        .rejects.toThrow(ValidationError);
    });
  });
});

describe('Calculator', () => {
  describe('add', () => {
    it.each([
      [1, 2, 3],
      [0, 0, 0],
      [-1, 1, 0],
      [100, 200, 300]
    ])('add(%i, %i) should return %i', (a, b, expected) => {
      expect(Calculator.add(a, b)).toBe(expected);
    });
  });
  
  describe('divide', () => {
    it('should throw error when dividing by zero', () => {
      expect(() => Calculator.divide(10, 0)).toThrow('Division by zero');
    });
  });
});
```

### 2. pytest (Python)

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def user_service(mock_repository):
    from services import UserService
    return UserService(mock_repository)

class TestUserService:
    """User service unit tests"""
    
    def test_get_user_by_id_success(self, user_service, mock_repository):
        mock_repository.find_by_id.return_value = {
            'id': '1',
            'name': 'John',
            'email': 'john@example.com'
        }
        
        result = user_service.get_user_by_id('1')
        
        assert result['name'] == 'John'
        mock_repository.find_by_id.assert_called_once_with('1')
    
    def test_get_user_by_id_not_found(self, user_service, mock_repository):
        mock_repository.find_by_id.return_value = None
        
        with pytest.raises(NotFoundError, match="User not found"):
            user_service.get_user_by_id('999')
    
    def test_create_user_validates_email(self, user_service):
        with pytest.raises(ValidationError, match="Invalid email"):
            user_service.create_user({
                'name': 'John',
                'email': 'invalid-email'
            })

@pytest.mark.parametrize("input,expected", [
    ({"a": 1, "b": 2}, 3),
    ({"a": 0, "b": 0}, 0),
    ({"a": -1, "b": 1}, 0),
    ({"a": 100, "b": 200}, 300),
])
def test_add_parametrized(input, expected):
    assert Calculator.add(input["a"], input["b"]) == expected

@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result is not None

class TestWithPatching:
    """Tests using patch decorator"""
    
    @patch('module.external_api_call')
    def test_with_mock(self, mock_api):
        mock_api.return_value = {'status': 'ok'}
        
        result = function_under_test()
        
        assert result['status'] == 'ok'
        mock_api.assert_called_once()
    
    @patch('module.datetime')
    def test_time_dependent(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0, 0)
        
        result = time_sensitive_function()
        
        assert result['timestamp'] == '2025-01-01T12:00:00'
```

### 3. Go Testing

```go
package service

import (
    "errors"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
    "github.com/stretchr/testify/require"
)

type MockRepository struct {
    mock.Mock
}

func (m *MockRepository) FindByID(id string) (*User, error) {
    args := m.Called(id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func TestUserService_GetUserByID_Success(t *testing.T) {
    mockRepo := new(MockRepository)
    service := NewUserService(mockRepo)
    
    expectedUser := &User{ID: "1", Name: "John", Email: "john@example.com"}
    mockRepo.On("FindByID", "1").Return(expectedUser, nil)
    
    user, err := service.GetUserByID("1")
    
    require.NoError(t, err)
    assert.Equal(t, "John", user.Name)
    mockRepo.AssertExpectations(t)
}

func TestUserService_GetUserByID_NotFound(t *testing.T) {
    mockRepo := new(MockRepository)
    service := NewUserService(mockRepo)
    
    mockRepo.On("FindByID", "999").Return(nil, ErrNotFound)
    
    user, err := service.GetUserByID("999")
    
    require.Error(t, err)
    assert.True(t, errors.Is(err, ErrNotFound))
    assert.Nil(t, user)
    mockRepo.AssertExpectations(t)
}

func TestCalculator_Add(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 1, 2, 3},
        {"zero values", 0, 0, 0},
        {"negative numbers", -1, 1, 0},
        {"large numbers", 100, 200, 300},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            assert.Equal(t, tt.expected, result)
        })
    }
}

func TestCalculator_Divide_ByZero(t *testing.T) {
    _, err := Divide(10, 0)
    
    require.Error(t, err)
    assert.Contains(t, err.Error(), "division by zero")
}

func BenchmarkUserService_GetUserByID(b *testing.B) {
    mockRepo := new(MockRepository)
    service := NewUserService(mockRepo)
    mockRepo.On("FindByID", "1").Return(&User{ID: "1"}, nil)
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        service.GetUserByID("1")
    }
}
```

### 4. JUnit (Java)

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("UserService Unit Tests")
class UserServiceTest {
    
    @Mock
    private UserRepository repository;
    
    @InjectMocks
    private UserService userService;
    
    private AutoCloseable mocks;
    
    @BeforeEach
    void setUp() {
        mocks = MockitoAnnotations.openMocks(this);
    }
    
    @AfterEach
    void tearDown() throws Exception {
        mocks.close();
    }
    
    @Nested
    @DisplayName("getUserById")
    class GetUserByIdTests {
        
        @Test
        @DisplayName("should return user when found")
        void shouldReturnUserWhenFound() {
            User expected = new User("1", "John", "john@example.com");
            when(repository.findById("1")).thenReturn(Optional.of(expected));
            
            User result = userService.getUserById("1");
            
            assertNotNull(result);
            assertEquals("John", result.getName());
            verify(repository).findById("1");
        }
        
        @Test
        @DisplayName("should throw exception when not found")
        void shouldThrowExceptionWhenNotFound() {
            when(repository.findById("999")).thenReturn(Optional.empty());
            
            assertThrows(NotFoundException.class, () -> {
                userService.getUserById("999");
            });
        }
        
        @ParameterizedTest
        @ValueSource(strings = {"", "  ", "null"})
        @DisplayName("should throw exception for invalid id")
        void shouldThrowExceptionForInvalidId(String id) {
            assertThrows(ValidationException.class, () -> {
                userService.getUserById(id);
            });
            
            verify(repository, never()).findById(any());
        }
    }
    
    @ParameterizedTest
    @CsvSource({
        "1, 2, 3",
        "0, 0, 0",
        "-1, 1, 0",
        "100, 200, 300"
    })
    @DisplayName("add should return correct sum")
    void addShouldReturnCorrectSum(int a, int b, int expected) {
        assertEquals(expected, Calculator.add(a, b));
    }
}
```

## 测试模式

### AAA模式 (Arrange-Act-Assert)

```javascript
it('should calculate total with discount', () => {
  // Arrange
  const cart = new Cart();
  cart.addItem({ price: 100 });
  cart.addItem({ price: 50 });
  const discount = 0.1;
  
  // Act
  const total = cart.calculateTotal(discount);
  
  // Assert
  expect(total).toBe(135);
});
```

### Given-When-Then模式

```python
def test_user_registration():
    # Given
    user_data = {"name": "John", "email": "john@example.com"}
    mock_db = Mock()
    
    # When
    result = register_user(user_data, mock_db)
    
    # Then
    assert result.success is True
    mock_db.insert.assert_called_once()
```

### Mock模式

```javascript
const mockDependencies = {
  api: {
    fetch: jest.fn(),
    post: jest.fn()
  },
  logger: {
    info: jest.fn(),
    error: jest.fn()
  }
};
```

## 最佳实践

1. **隔离性**: 每个测试独立运行，不依赖其他测试
2. **可重复性**: 测试结果稳定一致
3. **快速执行**: 单元测试应该毫秒级完成
4. **单一职责**: 每个测试只验证一个行为
5. **命名清晰**: 测试名描述预期行为
6. **边界测试**: 覆盖边界条件和异常情况
7. **Mock外部依赖**: 隔离外部系统

## 相关技能

- [integration-test](../integration-test) - 集成测试
- [e2e-test](../e2e-test) - 端到端测试
- [test-generator](../../actions/test/test-generator) - 测试生成
- [code-coverage](../../actions/test/code-coverage) - 覆盖率分析
