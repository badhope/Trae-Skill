---
name: react-native
description: "React Native mobile development expert for cross-platform apps. Keywords: react native, mobile, ios, android, expo, 跨平台, 移动开发"
layer: domain
role: specialist
version: 2.0.0
domain: mobile
languages:
  - javascript
  - typescript
frameworks:
  - react-native
  - expo
  - react-navigation
invoked_by:
  - coding-workflow
  - code-generator
capabilities:
  - cross_platform_development
  - native_modules
  - navigation
  - state_management
  - push_notifications
---

# React Native

React Native跨平台移动开发专家，使用JavaScript/TypeScript构建iOS和Android原生应用。

## 适用场景

- 跨平台移动应用
- MVP快速开发
- 现有Web应用移动化
- 原生模块集成
- 推送通知集成

## 核心架构

### 项目结构

```
src/
├── components/           # 可复用组件
│   ├── common/          # 通用组件
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   └── features/        # 功能组件
│       ├── UserCard.tsx
│       └── ProductList.tsx
├── screens/             # 页面
│   ├── auth/
│   │   ├── LoginScreen.tsx
│   │   └── RegisterScreen.tsx
│   ├── home/
│   │   └── HomeScreen.tsx
│   └── profile/
│       └── ProfileScreen.tsx
├── navigation/          # 导航配置
│   ├── AppNavigator.tsx
│   ├── AuthNavigator.tsx
│   └── MainNavigator.tsx
├── services/            # API服务
│   ├── api.ts
│   ├── auth.ts
│   └── storage.ts
├── hooks/               # 自定义Hooks
│   ├── useAuth.ts
│   └── useTheme.ts
├── store/               # 状态管理
│   ├── index.ts
│   ├── slices/
│   └── middleware/
├── utils/               # 工具函数
│   ├── helpers.ts
│   └── constants.ts
├── types/               # 类型定义
│   └── index.ts
└── theme/               # 主题配置
    ├── colors.ts
    └── typography.ts
```

### 导航配置

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function AuthNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        animation: 'slide_from_right'
      }}
    >
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="ForgotPassword" component={ForgotPasswordScreen} />
    </Stack.Navigator>
  );
}

function MainNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;
          
          switch (route.name) {
            case 'Home':
              iconName = focused ? 'home' : 'home-outline';
              break;
            case 'Search':
              iconName = focused ? 'search' : 'search-outline';
              break;
            case 'Cart':
              iconName = focused ? 'cart' : 'cart-outline';
              break;
            case 'Profile':
              iconName = focused ? 'person' : 'person-outline';
              break;
            default:
              iconName = 'ellipse';
          }
          
          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
        headerShown: false
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Cart" component={CartScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

function AppNavigator() {
  const { isAuthenticated } = useAuth();
  
  return (
    <NavigationContainer>
      {isAuthenticated ? <MainNavigator /> : <AuthNavigator />}
    </NavigationContainer>
  );
}
```

### 状态管理 (Redux Toolkit + RTK Query)

```typescript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { configureStore } from '@reduxjs/toolkit';

interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials: (state, action: PayloadAction<{ user: User; token: string }>) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.isAuthenticated = true;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
    }
  }
});

export const { setCredentials, logout } = authSlice.actions;

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: 'https://api.example.com',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    }
  }),
  tagTypes: ['User', 'Product', 'Order'],
  endpoints: (builder) => ({
    getProducts: builder.query<Product[], void>({
      query: () => '/products',
      providesTags: ['Product']
    }),
    getProduct: builder.query<Product, string>({
      query: (id) => `/products/${id}`,
      providesTags: (_, __, id) => [{ type: 'Product', id }]
    }),
    createOrder: builder.mutation<Order, CreateOrderRequest>({
      query: (body) => ({
        url: '/orders',
        method: 'POST',
        body
      }),
      invalidatesTags: ['Order']
    })
  })
});

export const { useGetProductsQuery, useGetProductQuery, useCreateOrderMutation } = apiSlice;

export const store = configureStore({
  reducer: {
    auth: authSlice.reducer,
    [apiSlice.reducerPath]: apiSlice.reducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware)
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 组件示例

```typescript
import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Image,
  ActivityIndicator,
  RefreshControl
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useGetProductsQuery } from '../store';

interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
  description: string;
}

interface ProductListProps {
  category?: string;
}

export const ProductList: React.FC<ProductListProps> = ({ category }) => {
  const navigation = useNavigation();
  const { data: products, isLoading, error, refetch } = useGetProductsQuery();
  
  const renderProduct = ({ item }: { item: Product }) => (
    <TouchableOpacity
      style={styles.productCard}
      onPress={() => navigation.navigate('ProductDetail', { id: item.id })}
    >
      <Image
        source={{ uri: item.image }}
        style={styles.productImage}
        resizeMode="cover"
      />
      <View style={styles.productInfo}>
        <Text style={styles.productName} numberOfLines={2}>
          {item.name}
        </Text>
        <Text style={styles.productPrice}>
          ${item.price.toFixed(2)}
        </Text>
      </View>
    </TouchableOpacity>
  );
  
  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }
  
  if (error) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorText}>Failed to load products</Text>
        <TouchableOpacity style={styles.retryButton} onPress={refetch}>
          <Text style={styles.retryText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }
  
  return (
    <FlatList
      data={products}
      renderItem={renderProduct}
      keyExtractor={(item) => item.id}
      numColumns={2}
      contentContainerStyle={styles.listContainer}
      refreshControl={
        <RefreshControl
          refreshing={isLoading}
          onRefresh={refetch}
          colors={['#007AFF']}
        />
      }
    />
  );
};

const styles = StyleSheet.create({
  listContainer: {
    padding: 8
  },
  productCard: {
    flex: 1,
    margin: 8,
    backgroundColor: '#fff',
    borderRadius: 12,
    overflow: 'hidden',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4
  },
  productImage: {
    width: '100%',
    height: 150
  },
  productInfo: {
    padding: 12
  },
  productName: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4
  },
  productPrice: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#007AFF'
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  },
  errorText: {
    fontSize: 16,
    color: '#666',
    marginBottom: 16
  },
  retryButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8
  },
  retryText: {
    color: '#fff',
    fontWeight: '600'
  }
});
```

### 原生模块

```typescript
import { NativeModules, NativeEventEmitter, Platform } from 'react-native';

const { RNBluetoothManager } = NativeModules;

interface BluetoothDevice {
  id: string;
  name: string;
  rssi: number;
}

class BluetoothModule {
  private eventEmitter: NativeEventEmitter;
  
  constructor() {
    this.eventEmitter = new NativeEventEmitter(RNBluetoothManager);
  }
  
  async isBluetoothEnabled(): Promise<boolean> {
    return RNBluetoothManager.isBluetoothEnabled();
  }
  
  async enableBluetooth(): Promise<void> {
    return RNBluetoothManager.enableBluetooth();
  }
  
  async scanForDevices(timeout: number = 10): Promise<BluetoothDevice[]> {
    return RNBluetoothManager.scanForDevices(timeout);
  }
  
  async connectToDevice(deviceId: string): Promise<void> {
    return RNBluetoothManager.connectToDevice(deviceId);
  }
  
  onDeviceFound(callback: (device: BluetoothDevice) => void): () => void {
    const subscription = this.eventEmitter.addListener(
      'onDeviceFound',
      callback
    );
    return () => subscription.remove();
  }
  
  onConnectionStateChanged(callback: (state: string) => void): () => void {
    const subscription = this.eventEmitter.addListener(
      'onConnectionStateChanged',
      callback
    );
    return () => subscription.remove();
  }
}

export default new BluetoothModule();
```

### 推送通知

```typescript
import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true
  })
});

class NotificationService {
  async registerForPushNotifications(): Promise<string | null> {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    
    if (finalStatus !== 'granted') {
      return null;
    }
    
    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF231F7C'
      });
    }
    
    const token = await Notifications.getExpoPushTokenAsync({
      projectId: 'your-project-id'
    });
    
    return token.data;
  }
  
  async scheduleLocalNotification(
    title: string,
    body: string,
    seconds: number
  ): Promise<string> {
    return Notifications.scheduleNotificationAsync({
      content: {
        title,
        body,
        sound: true,
        priority: Notifications.AndroidNotificationPriority.HIGH
      },
      trigger: { seconds }
    });
  }
  
  addNotificationReceivedListener(
    callback: (notification: Notifications.Notification) => void
  ): Notifications.EventSubscription {
    return Notifications.addNotificationReceivedListener(callback);
  }
  
  addNotificationResponseReceivedListener(
    callback: (response: Notifications.NotificationResponse) => void
  ): Notifications.EventSubscription {
    return Notifications.addNotificationResponseReceivedListener(callback);
  }
}

export default new NotificationService();
```

## 最佳实践

1. **性能优化**: 使用FlatList的虚拟化、避免不必要的重渲染
2. **样式**: 使用StyleSheet.create而非内联样式
3. **导航**: 使用类型安全的导航
4. **状态管理**: Redux Toolkit + RTK Query
5. **错误处理**: 全局错误边界
6. **测试**: Jest + React Native Testing Library
7. **CI/CD**: EAS Build和Submit

## 相关技能

- [frontend-react](../frontend/react) - React Web开发
- [flutter](../flutter) - Flutter开发
- [unit-test](../testing/unit-test) - 单元测试
- [e2e-test](../testing/e2e-test) - E2E测试
