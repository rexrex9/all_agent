"use client";

import { useState, FormEvent, Suspense } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { createClient } from "@/providers/client";
import { useQueryState } from "nuqs";
import { toast } from "sonner";
import { LangGraphLogoSVG } from "@/components/icons/langgraph";
import { useRouter } from "next/navigation";

interface AssistantCreateForm {
  assistantId?: string;
}

function CreateAssistantContent() {
  const router = useRouter();
  const [apiUrl, setApiUrl] = useQueryState("apiUrl");
  const [apiKey, setApiKey] = useState("");
  const [form, setForm] = useState<AssistantCreateForm>({
    assistantId: "",
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const client = createClient(apiUrl || "", apiKey);
      // 使用默认值创建assistant，只需要assistantId
      const assistant = await client.assistants.create({
        graphId: "agent", // 默认graphId
        name: form.assistantId || "default-assistant", // 使用assistantId作为name，或者默认名称
        description: "Default assistant created from UI", // 默认描述
        assistantId: form.assistantId,
        ifExists: "do_nothing", // 默认如果存在则不做任何操作
      });

      toast.success("Assistant created successfully!");
      console.log("Created assistant:", assistant);
      if (form.assistantId) {
          router.push(`/?assistantId=${encodeURIComponent(form.assistantId)}`);
      } else {
          router.push('/');
      }

    } catch (error) {
      toast.error("Failed to create assistant");
      console.error("Error creating assistant:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <LangGraphLogoSVG className="h-8 flex-shrink-0" />
            <h1 className="text-2xl font-semibold tracking-tight">Create Assistant</h1>
          </div>
        </div>
      </div>

      <div className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="p-6">
            <h2 className="text-lg font-medium mb-4">Assistant Configuration</h2>
            <form onSubmit={handleSubmit} className="grid gap-4">
              <div className="grid gap-2">
                <Label htmlFor="assistantId">Assistant ID <span className="text-red-500">*</span></Label>
                <Input
                  id="assistantId"
                  name="assistantId"
                  value={form.assistantId}
                  onChange={handleChange}
                  placeholder="Enter assistant ID"
                  required
                />
              </div>
              <div className="flex justify-end">
                <Button type="submit" disabled={isLoading}>
                  {isLoading ? "Creating..." : "Create Assistant"}
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function CreateAssistantPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-gray-50 flex items-center justify-center">Loading...</div>}>
      <CreateAssistantContent />
    </Suspense>
  );
}