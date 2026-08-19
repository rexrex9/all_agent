## Agent Chat UI

该项目基于 [langchain-ai/agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui) 做了少量自定义的修改。

启动方式与详细介绍可参阅 [README_OLD.md](README_OLD.md)

## 改动处

1. 原来仅可接收pdf与图片文件改为了可接收所有文件。
2. 修改了logo与标题。
3. 英文都改成了中文。

## 自定义标题

若需自定义标题，则在 src/config.ts 文件中修改 APP_CONFIG.name的值。

## 自定义logo

logo采用的是svg格式，需将logo的svg内容黏贴于 src/components/icons/langgraph.tsx 文件的 return 处(覆盖原有内容。)

假设某个svg内容如下：

```xml
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width={width} height={height} preserveAspectRatio="none" className={className}>
<path transform="translate(0,0)" fill="rgb(255,255,255)" d="M 0 0 L 2048 0 L 2048 2048 L 0 2048 L 0 0 z"/>
....
....
</svg>
```

则 src/components/icons/langgraph.tsx 文件的内容覆盖后如下：

```xml
export function LangGraphLogoSVG({
  className,
  width,
  height,
}: {
  width?: number;
  height?: number;
  className?: string;
}) {
  return (
	<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width={width} height={height} preserveAspectRatio="none" className={className}>
<path transform="translate(0,0)" fill="rgb(255,255,255)" d="M 0 0 L 2048 0 L 2048 2048 L 0 2048 L 0 0 z"/>
....
....
</svg>
  );
}
```









