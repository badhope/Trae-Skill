import { createMCPServer } from '../../packages/core/mcp/builder'

const 藏头诗库 = {
  爱: ['爱君乐事佳兴发', '爱人传经心事违', '爱惜长条待少年', '爱子临风吹玉笛'],
  情: ['情知此会生春梦', '情天情海幻情深', '情著春风生橘树', '情知万法本来空'],
  一: ['一回思念一眉颦', '一生一世永爱你', '一点寒光万丈芒', '一笑相逢情自亲'],
  生: ['生子笔力能巧妙', '生人情谊贵和光', '生平不得春风力', '生意满怀都是春'],
  平: ['平生风义兼师友', '平生志 Native 在神仙', '平步青云应不到', '平生豪气干牛斗'],
  安: ['安上文书信手翻', '安得四海中蟾窟', '安车正好追先烈', '安康使君发成都'],
  喜: ['喜见东风扬水花', '喜欢得伴山僧宿', '喜见通贤家子弟', '喜君眸子重清朗'],
  乐: ['乐事只今惟有酒', '乐天才思如春雨', '乐事也知存后会', '乐广青天幸未开'],
  顺: ['顺阳门外看新晴', '顺熟合依元白体', '顺理以观皆有趣', '顺流一日快舟行'],
  利: ['利名场里合抽身', '利达真成驷马过', '利名那得羡锱铢', '利锁名缰更惑人']
}

const 彩虹屁 = [
  '你今天的气质也太绝了吧！简直就是行走的画报！',
  '这是什么级别的仙女下凡啊，请停止你的美貌杀人！',
  '你的颜值就应该放在国家博物馆供起来，每天三拜九叩！',
  '我严重怀疑你是吃美貌长大的，怎么能好看得这么不科学！',
  '以你的颜值，不出道真的太可惜了，娱乐圈需要你！',
  '今天的美貌也认真营业了呢！完美到我找不到词形容！',
  '你这张脸建议申遗，这是人类美学的奇迹！',
  '美貌鲨人事件又发生了，凶手就是你！',
  '你往那儿一站就是风景本人，还看什么山看什么海！',
  '真的太绝了，你是吃神仙水长大的吗？',
  '上帝制造你的时候一定花了120%的心思！',
  '这种程度的颜值真的是真实存在的吗？我不是在做梦吧！',
  '求你别再散发魅力了，我已经完全被你迷住了！',
  '有颜有才说的就是你吧，上帝到底给你关了哪扇窗？',
  '你就是人间理想型本型！'
]

const 毒鸡汤 = [
  '条条大路通罗马，可有人就生在罗马。',
  '世上无难事，只要肯放弃。',
  '努力不一定成功，但不努力一定很轻松。',
  '万事开头难，然后中间难，最后结尾难。',
  '只要是石头，到哪里都不会发光的。',
  '失败是成功之母，可惜成功六亲不认。',
  '上帝为你关上一扇门，然后就去睡觉了。',
  '有时候你不努力一下，都不知道什么叫绝望。',
  '现在的人太着急了，其实慢慢熬，早晚都会熬出头的...就是有点秃。',
  '人生就是起起落落落落落落落落落落。',
  '你总说自己过得不好，一上秤又胖了不少。',
  '当你觉得自己又穷又丑的时候，不要悲伤，至少你的判断是对的。',
  '比你优秀的人都在努力，你努力还有什么用。',
  '生活不止眼前的苟且，还有读不懂的诗和到不了的远方。',
  '不要看别人表面上一帆风顺，实际上他们背地里，也是一帆风顺。'
]

const 谐音梗 = [
  { question: '什么动物最容易摔倒？', answer: '狐狸，因为狐狸狡猾（脚滑）。' },
  { question: '什么水果最怕热？', answer: '芒果（忙过）。' },
  { question: '什么数字最听话？', answer: '100，因为百依百顺。' },
  { question: '什么马不会跑？', answer: '木马。' },
  { question: '什么水永远用不完？', answer: '口水。' },
  { question: '什么东西有五个头，但人不觉得它怪？', answer: '手和脚。' },
  { question: '布和纸怕什么？', answer: '布（不）怕一万，纸（只）怕万一。' },
  { question: '铅笔姓什么？', answer: '萧，因为削（萧）铅笔。' },
  { question: '从1到9哪个数字最勤劳？', answer: '1懒惰，2勤劳。因为一（1）不做二（2）不休。' },
  { question: '怎样使麻雀安静下来？', answer: '压它一下。因为鸦雀无声（压雀无声）。' },
  { question: '历史上哪个人跑的最快？', answer: '曹操，说曹操曹操到。' },
  { question: '小白加小白等于什么？', answer: '小白兔（TWO）。' },
  { question: '30-50哪个数字比熊的大便厉害？', answer: '40，因为事实（40）胜于雄辩（熊便）。' },
  { question: '什么东西最会把持不住？', answer: '海马，因为上海马体（上海马体）。' },
  { question: '哪个地方的人手机最爱关机？', answer: '宁波，因为（您拨）打的电话已关机。' }
]

const 土味情话 = [
  '我对你的爱，就像拖拉机上山，轰轰烈烈。',
  '你知道我最喜欢什么酒吗？什么酒？和你的天长地久。',
  '我觉得你特别像一款游戏。什么游戏？我的世界。',
  '你最近是不是又胖了？那你为什么在我心里的分量越来越重了？',
  '我点的东西怎么还没来？什么东西？我们的未来。',
  '你知道你和星星有什么区别吗？星星在天上，你在我心里。',
  '你知道我想成为什么人吗？什么人？你的人。',
  '你可以帮我洗个东西吗？洗什么？喜欢我。',
  '现在几点了？是我们幸福的起点。',
  '我是可爱的女孩子，你是可爱。',
  '我最近学会了一门新技能，算命。我掐指一算，你命里缺我。',
  '你属什么？虎。不，你属于我。',
  '我觉得你今天怪怪的。哪里怪？怪好看的。',
  '你的脸上有点东西。有什么？有点漂亮。',
  '我有一个超能力。是什么？超喜欢你。'
]

const 脑筋急转弯 = [
  { question: '什么东西明明是你的，别人却用得比你多？', answer: '你的名字。' },
  { question: '什么东西越洗越脏？', answer: '水。' },
  { question: '什么路最窄？', answer: '冤家路窄。' },
  { question: '什么东西没吃的时候是绿的，吃的时候是红的，吐出来的是黑的？', answer: '西瓜。' },
  { question: '什么事睁一只眼闭一只眼比较好？', answer: '射击。' },
  { question: '什么人一年中只工作一天？', answer: '圣诞老人。' },
  { question: '什么东西打破了才能吃？', answer: '鸡蛋。' },
  { question: '什么门永远关不上？', answer: '球门。' },
  { question: '什么书你不可能在书店里买到？', answer: '秘书。' },
  { question: '什么东西只能加不能减？', answer: '年龄。' },
  { question: '什么东西越热越爱出来？', answer: '汗。' },
  { question: '什么东西有脚却不能走路？', answer: '桌子椅子。' },
  { question: '什么球离你最近？', answer: '眼球。' },
  { question: '什么房子失了火却不见有人跑出来？', answer: '太平间。' },
  { question: '什么样的速度最快？', answer: '一步登天。' }
]

const 成语 = [
  '一心一意', '意气风发', '发扬光大', '大功告成', '成千上万',
  '万众一心', '心想事成', '成家立业', '业精于勤', '勤能补拙',
  '拙口笨舌', '舌战群儒', '儒雅风流', '流连忘返', '返璞归真',
  '真心实意', '异想天开', '开门见山', '山高水长', '长长久久',
  '九牛一毛', '毛手毛脚', '脚踏实地', '地久天长', '长命百岁',
  '岁岁平安', '安居乐业', '夜以继日', '日新月异', '异口同声',
  '声东击西', '西装革履', '屡战屡胜', '胜利在望', '望子成龙',
  '龙马精神', '神采飞扬', '扬眉吐气', '气宇轩昂', '昂首挺胸'
]

export default createMCPServer({
  name: 'fun',
  version: '1.0.0',
  description: '趣味特色工具集 - 藏头诗、彩虹屁、毒鸡汤、谐音梗、土味情话、脑筋急转弯',
  author: 'MCP Expert Community',
  icon: '🎉'
})
  .addTool({
    name: 'acrostic_poem',
    description: '生成藏头诗',
    parameters: {
      words: { type: 'string', description: '藏头词（如：我爱中国）', required: true },
      style: { type: 'string', description: '风格: 爱情, 祝福, 励志, 友情', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const words = String(params.words || '')
      const chars = [...words]
      const lines: string[] = []
      chars.forEach((char, idx) => {
        const options = (藏头诗库 as any)[char]
        if (options) {
          lines.push(options[idx % options.length])
        } else {
          lines.push(`${char}字句生成中...`)
        }
      })
      return {
        success: true,
        words,
        style: params.style || '通用',
        poem: lines,
        note: '以上为半首藏头诗示例，完整版需要完整诗词库支持'
      }
    }
  })
  .addTool({
    name: 'rainbow_fart',
    description: '彩虹屁生成器',
    parameters: {
      count: { type: 'number', description: '生成数量', required: false },
      topic: { type: 'string', description: '主题: 颜值, 才华, 气质, 人品', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const count = Number(params.count) || 3
      const shuffled = [...彩虹屁].sort(() => Math.random() - 0.5)
      return {
        success: true,
        count,
        topic: params.topic || '通用',
        sentences: shuffled.slice(0, count)
      }
    }
  })
  .addTool({
    name: 'toxic_chicken_soup',
    description: '毒鸡汤生成器',
    parameters: {
      count: { type: 'number', description: '生成数量', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const count = Number(params.count) || 3
      const shuffled = [...毒鸡汤].sort(() => Math.random() - 0.5)
      return {
        success: true,
        count,
        sentences: shuffled.slice(0, count)
      }
    }
  })
  .addTool({
    name: 'homophonic_joke',
    description: '谐音梗生成器',
    parameters: {
      count: { type: 'number', description: '生成数量', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const count = Number(params.count) || 3
      const shuffled = [...谐音梗].sort(() => Math.random() - 0.5)
      return {
        success: true,
        count,
        jokes: shuffled.slice(0, count)
      }
    }
  })
  .addTool({
    name: 'cheesy_love_lines',
    description: '土味情话生成器',
    parameters: {
      count: { type: 'number', description: '生成数量', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const count = Number(params.count) || 3
      const shuffled = [...土味情话].sort(() => Math.random() - 0.5)
      return {
        success: true,
        count,
        lines: shuffled.slice(0, count)
      }
    }
  })
  .addTool({
    name: 'brain_teaser',
    description: '脑筋急转弯',
    parameters: {
      count: { type: 'number', description: '生成数量', required: false },
      showAnswer: { type: 'boolean', description: '是否显示答案', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const count = Number(params.count) || 3
      const showAnswer = params.showAnswer !== false
      const shuffled = [...脑筋急转弯].sort(() => Math.random() - 0.5)
      const result = shuffled.slice(0, count).map(item => ({
        question: item.question,
        answer: showAnswer ? item.answer : '（点击显示答案）'
      }))
      return {
        success: true,
        count,
        showAnswer,
        teasers: result
      }
    }
  })
  .addTool({
    name: 'idiom_solitaire',
    description: '成语接龙',
    parameters: {
      start: { type: 'string', description: '起始成语', required: true },
      count: { type: 'number', description: '接龙数量', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const start = String(params.start || '一心一意')
      const count = Number(params.count) || 5
      const chain: string[] = [start]
      let lastChar = start[start.length - 1]
      for (let i = 0; i < count - 1; i++) {
        const next = 成语.find(c => c[0] === lastChar && !chain.includes(c))
        if (next) {
          chain.push(next)
          lastChar = next[next.length - 1]
        } else {
          break
        }
      }
      return {
        success: true,
        start,
        chainLength: chain.length,
        chain
      }
    }
  })
  .addTool({
    name: 'emoji_translate',
    description: 'emoji表情翻译',
    parameters: {
      text: { type: 'string', description: '要翻译的文字', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const emojiMap: Record<string, string> = {
        '开心': '😄', '快乐': '🎉', '喜欢': '😍', '爱': '❤️', '哭': '😭',
        '生气': '😠', '加油': '💪', '厉害': '👍', '牛': '🐂', '钱': '💰',
        '火': '🔥', '水': '💧', '星星': '⭐', '月亮': '🌙', '太阳': '☀️',
        '花': '🌸', '心': '💖', '好': '✅', '不': '❌', '问号': '❓'
      }
      let result = String(params.text || '')
      Object.entries(emojiMap).forEach(([word, emoji]) => {
        result = result.split(word).join(emoji)
      })
      return {
        success: true,
        original: params.text,
        translated: result
      }
    }
  })
  .build()
