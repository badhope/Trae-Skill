---
name: mongodb
description: "MongoDB database development with schema design, aggregation, and optimization. Keywords: mongodb, nosql, aggregation, mongoose, 文档数据库"
layer: domain
role: specialist
version: 2.0.0
domain: database
languages:
  - javascript
  - typescript
frameworks:
  - mongoose
  - mongodb-driver
invoked_by:
  - coding-workflow
  - database-migration
capabilities:
  - schema_design
  - aggregation_pipeline
  - indexing_strategy
  - performance_optimization
  - data_modeling
---

# MongoDB

MongoDB文档数据库专家，专注于Schema设计、聚合管道和性能优化。

## 适用场景

- 文档型数据存储
- 灵活Schema需求
- 高并发读写
- 地理位置应用
- 内容管理系统

## 核心架构

### 1. Mongoose Schema设计

```typescript
import mongoose, { Schema, Document, Model } from 'mongoose';

interface IUser extends Document {
  email: string;
  name: string;
  avatar?: string;
  status: 'active' | 'inactive' | 'suspended';
  roles: string[];
  profile: {
    bio?: string;
    location?: string;
    website?: string;
  };
  lastLoginAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}

const UserSchema = new Schema<IUser>(
  {
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
      index: true,
    },
    name: {
      type: String,
      required: true,
      trim: true,
      maxlength: 100,
    },
    avatar: {
      type: String,
      trim: true,
    },
    status: {
      type: String,
      enum: ['active', 'inactive', 'suspended'],
      default: 'active',
      index: true,
    },
    roles: [{
      type: String,
      enum: ['user', 'admin', 'moderator'],
      default: 'user',
    }],
    profile: {
      bio: { type: String, maxlength: 500 },
      location: { type: String, maxlength: 100 },
      website: { type: String },
    },
    lastLoginAt: {
      type: Date,
      index: true,
    },
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

UserSchema.virtual('posts', {
  ref: 'Post',
  localField: '_id',
  foreignField: 'author',
  justOne: false,
});

UserSchema.index({ name: 'text', email: 'text' });

UserSchema.pre('save', function (next) {
  if (this.isModified('email')) {
    this.email = this.email.toLowerCase();
  }
  next();
});

UserSchema.methods.toJSON = function () {
  const user = this.toObject();
  delete user.password;
  delete user.__v;
  return user;
};

UserSchema.statics.findByEmail = function (email: string) {
  return this.findOne({ email: email.toLowerCase() });
};

UserSchema.statics.findActive = function () {
  return this.find({ status: 'active' });
};

export const User = mongoose.model<IUser>('User', UserSchema);

interface IPost extends Document {
  title: string;
  content: string;
  author: mongoose.Types.ObjectId;
  tags: string[];
  status: 'draft' | 'published';
  publishedAt?: Date;
  viewCount: number;
  likeCount: number;
  comments: IComment[];
  createdAt: Date;
  updatedAt: Date;
}

const PostSchema = new Schema<IPost>(
  {
    title: {
      type: String,
      required: true,
      trim: true,
      maxlength: 200,
    },
    content: {
      type: String,
      required: true,
    },
    author: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      index: true,
    },
    tags: [{
      type: String,
      trim: true,
      lowercase: true,
      index: true,
    }],
    status: {
      type: String,
      enum: ['draft', 'published'],
      default: 'draft',
      index: true,
    },
    publishedAt: {
      type: Date,
      index: true,
    },
    viewCount: {
      type: Number,
      default: 0,
      min: 0,
    },
    likeCount: {
      type: Number,
      default: 0,
      min: 0,
    },
    comments: [{
      content: { type: String, required: true },
      author: { type: Schema.Types.ObjectId, ref: 'User', required: true },
      createdAt: { type: Date, default: Date.now },
    }],
  },
  {
    timestamps: true,
  }
);

PostSchema.index({ title: 'text', content: 'text' });
PostSchema.index({ author: 1, status: 1, createdAt: -1 });
PostSchema.index({ tags: 1, publishedAt: -1 });

export const Post = mongoose.model<IPost>('Post', PostSchema);
```

### 2. 聚合管道

```typescript
class PostAggregation {
  static async getPostsWithAuthorStats(options: {
    page: number;
    limit: number;
    status?: string;
    tags?: string[];
  }) {
    const { page, limit, status, tags } = options;
    const skip = (page - 1) * limit;
    
    const match: any = {};
    if (status) match.status = status;
    if (tags?.length) match.tags = { $in: tags };
    
    const pipeline = [
      { $match: match },
      
      {
        $lookup: {
          from: 'users',
          localField: 'author',
          foreignField: '_id',
          as: 'authorData',
        },
      },
      
      { $unwind: '$authorData' },
      
      {
        $lookup: {
          from: 'comments',
          localField: '_id',
          foreignField: 'post',
          as: 'commentsData',
        },
      },
      
      {
        $addFields: {
          commentCount: { $size: '$commentsData' },
          authorName: '$authorData.name',
          authorEmail: '$authorData.email',
        },
      },
      
      {
        $project: {
          title: 1,
          content: 1,
          tags: 1,
          status: 1,
          viewCount: 1,
          likeCount: 1,
          commentCount: 1,
          authorName: 1,
          authorEmail: 1,
          createdAt: 1,
          publishedAt: 1,
        },
      },
      
      { $sort: { createdAt: -1 } },
      
      { $skip: skip },
      { $limit: limit },
    ];
    
    return Post.aggregate(pipeline);
  }
  
  static async getTagStatistics() {
    return Post.aggregate([
      { $unwind: '$tags' },
      
      {
        $group: {
          _id: '$tags',
          count: { $sum: 1 },
          totalViews: { $sum: '$viewCount' },
          totalLikes: { $sum: '$likeCount' },
          avgViews: { $avg: '$viewCount' },
        },
      },
      
      { $sort: { count: -1 } },
      
      {
        $project: {
          tag: '$_id',
          count: 1,
          totalViews: 1,
          totalLikes: 1,
          avgViews: { $round: ['$avgViews', 2] },
        },
      },
    ]);
  }
  
  static async getAuthorLeaderboard(limit: number = 10) {
    return Post.aggregate([
      { $match: { status: 'published' } },
      
      {
        $group: {
          _id: '$author',
          postCount: { $sum: 1 },
          totalViews: { $sum: '$viewCount' },
          totalLikes: { $sum: '$likeCount' },
          avgViews: { $avg: '$viewCount' },
        },
      },
      
      {
        $lookup: {
          from: 'users',
          localField: '_id',
          foreignField: '_id',
          as: 'author',
        },
      },
      
      { $unwind: '$author' },
      
      {
        $addFields: {
          score: {
            $add: [
              { $multiply: ['$postCount', 10] },
              { $multiply: ['$totalViews', 0.01] },
              { $multiply: ['$totalLikes', 0.5] },
            ],
          },
        },
      },
      
      { $sort: { score: -1 } },
      
      { $limit: limit },
      
      {
        $project: {
          authorName: '$author.name',
          authorEmail: '$author.email',
          postCount: 1,
          totalViews: 1,
          totalLikes: 1,
          avgViews: { $round: ['$avgViews', 2] },
          score: { $round: ['$score', 2] },
        },
      },
    ]);
  }
  
  static async getDailyStatistics(startDate: Date, endDate: Date) {
    return Post.aggregate([
      {
        $match: {
          createdAt: { $gte: startDate, $lte: endDate },
        },
      },
      
      {
        $group: {
          _id: {
            $dateToString: { format: '%Y-%m-%d', date: '$createdAt' },
          },
          postCount: { $sum: 1 },
          totalViews: { $sum: '$viewCount' },
          totalLikes: { $sum: '$likeCount' },
        },
      },
      
      { $sort: { _id: 1 } },
      
      {
        $project: {
          date: '$_id',
          postCount: 1,
          totalViews: 1,
          totalLikes: 1,
        },
      },
    ]);
  }
}
```

### 3. 索引策略

```typescript
class IndexManager {
  static async createIndexes() {
    await User.createIndexes();
    await Post.createIndexes();
    
    await mongoose.connection.db.collection('posts').createIndex(
      { title: 'text', content: 'text' },
      { 
        weights: {
          title: 10,
          content: 5,
        },
        name: 'post_text_search',
      }
    );
    
    await mongoose.connection.db.collection('posts').createIndex(
      { 'comments.createdAt': -1 },
      { sparse: true }
    );
    
    await mongoose.connection.db.collection('users').createIndex(
      { location: '2dsphere' },
      { sparse: true }
    );
  }
  
  static async getIndexes(collection: string) {
    return mongoose.connection.db.collection(collection).getIndexes();
  }
  
  static async dropIndex(collection: string, indexName: string) {
    return mongoose.connection.db.collection(collection).dropIndex(indexName);
  }
  
  static async analyzeQueryPerformance(query: any) {
    return Post.aggregate([
      { $match: query },
      { $explain: true },
    ]);
  }
}
```

### 4. 事务处理

```typescript
import { ClientSession } from 'mongoose';

class TransactionService {
  static async transferCredits(
    fromUserId: string,
    toUserId: string,
    amount: number
  ) {
    const session = await mongoose.startSession();
    
    try {
      session.startTransaction();
      
      const fromUser = await User.findById(fromUserId).session(session);
      const toUser = await User.findById(toUserId).session(session);
      
      if (!fromUser || !toUser) {
        throw new Error('User not found');
      }
      
      if ((fromUser as any).credits < amount) {
        throw new Error('Insufficient credits');
      }
      
      await User.updateOne(
        { _id: fromUserId },
        { $inc: { credits: -amount } }
      ).session(session);
      
      await User.updateOne(
        { _id: toUserId },
        { $inc: { credits: amount } }
      ).session(session);
      
      await Transaction.create([{
        from: fromUserId,
        to: toUserId,
        amount,
        type: 'transfer',
      }], { session });
      
      await session.commitTransaction();
      
      return { success: true };
    } catch (error) {
      await session.abortTransaction();
      throw error;
    } finally {
      session.endSession();
    }
  }
}
```

## 最佳实践

1. **Schema设计**: 嵌入vs引用的选择
2. **索引优化**: 根据查询模式创建索引
3. **聚合管道**: 使用管道进行复杂查询
4. **分页策略**: 使用skip+limit或游标分页
5. **事务使用**: 仅在必要时使用事务
6. **连接池**: 合理配置连接池大小

## 相关技能

- [database-migration](../database-migration) - 数据库迁移
- [sql-optimization](../sql-optimization) - SQL优化
- [backend-nodejs](../../backend/nodejs) - Node.js后端
