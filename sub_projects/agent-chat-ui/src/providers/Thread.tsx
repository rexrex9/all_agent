import { validate } from "uuid";
import { getApiKey } from "@/lib/api-key";
import { Thread } from "@langchain/langgraph-sdk";
import { useQueryState } from "nuqs";
import {
  createContext,
  useContext,
  ReactNode,
  useCallback,
  useState,
  Dispatch,
  SetStateAction,
  useEffect,
} from "react"; // 添加 useEffect
import { createClient } from "./client";

interface ThreadContextType {
  getThreads: () => Promise<Thread[]>;
  threads: Thread[];
  setThreads: Dispatch<SetStateAction<Thread[]>>;
  threadsLoading: boolean;
  setThreadsLoading: Dispatch<SetStateAction<boolean>>;
}

const ThreadContext = createContext<ThreadContextType | undefined>(undefined);

// Default values for API URL and Assistant ID
const DEFAULT_API_URL = "http://localhost:2024";
const DEFAULT_ASSISTANT_ID = "agent";

function getThreadSearchMetadata(
  assistantId: string,
): { graph_id: string } | { assistant_id: string } {
  if (validate(assistantId)) {
    return { assistant_id: assistantId };
  } else {
    return { graph_id: assistantId };
  }
}

export function ThreadProvider({ children }: { children: ReactNode }) {
  const [urlApiUrl] = useQueryState("apiUrl");
  const [urlAssistantId] = useQueryState("assistantId");
  const [threads, setThreads] = useState<Thread[]>([]);
  const [threadsLoading, setThreadsLoading] = useState(false);
  const [envVars, setEnvVars] = useState({
    apiUrl: "",
    assistantId: "",
  });

  // 从 API 获取环境变量
  useEffect(() => {
    const fetchEnvVars = async () => {
      try {
        const response = await fetch('/api/env');
        if (response.ok) {
          const data = await response.json();
          setEnvVars({
            apiUrl: data.API_URL || '',
            assistantId: data.ASSISTANT_ID || '',
          });
        }
      } catch (error) {
        console.error('Failed to fetch environment variables:', error);
      }
    };

    fetchEnvVars();
  }, []);

  // 优先级：URL 参数 > API 获取的环境变量 > 默认值
  const finalApiUrl = urlApiUrl || envVars.apiUrl || DEFAULT_API_URL;
  const finalAssistantId = urlAssistantId || envVars.assistantId || DEFAULT_ASSISTANT_ID;

  // 当API URL或Assistant ID变化时，清空线程列表以触发重新获取
  useEffect(() => {
    setThreads([]);
  }, [finalApiUrl, finalAssistantId]);

  // 移除 process.env 的直接引用
  console.log('ThreadProvider config:', {
    urlApiUrl,
    urlAssistantId,
    envVars,
    finalApiUrl,
    finalAssistantId
  });

  const getThreads = useCallback(async (): Promise<Thread[]> => {
    if (!finalApiUrl || !finalAssistantId) {
      console.warn('Missing API URL or Assistant ID for thread fetching');
      return [];
    }

    console.log('Fetching threads from:', finalApiUrl, 'with assistant:', finalAssistantId);

    try {
      const client = createClient(finalApiUrl, getApiKey() ?? undefined);

      const threads = await client.threads.search({
        metadata: {
          ...getThreadSearchMetadata(finalAssistantId),
        },
        limit: 100,
      });

      return threads;
    } catch (error) {
      console.error('Failed to fetch threads:', error);
      return [];
    }
  }, [finalApiUrl, finalAssistantId]);

  const value = {
    getThreads,
    threads,
    setThreads,
    threadsLoading,
    setThreadsLoading,
  };

  return (
    <ThreadContext.Provider value={value}>{children}</ThreadContext.Provider>
  );
}

export function useThreads() {
  const context = useContext(ThreadContext);
  if (context === undefined) {
    throw new Error("useThreads must be used within a ThreadProvider");
  }
  return context;
}
