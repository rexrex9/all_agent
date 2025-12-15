import { ContentBlock } from "@langchain/core/messages";
import { toast } from "sonner";

// Returns a Promise of a typed multimodal block for images, PDFs, or other files
export async function fileToContentBlock(
  file: File,
): Promise<ContentBlock.Multimodal.Data> {
  const supportedImageTypes = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
  ];

  if (supportedImageTypes.includes(file.type)) {
    // 图片类型：转换为 base64
    const data = await fileToBase64(file);
    return {
      type: "image",
      mimeType: file.type,
      data,
      metadata: { filename: file.name },
    };
  } else if (file.type === "application/pdf") {
    // PDF 类型：转换为 base64
    const data = await fileToBase64(file);
    return {
      type: "file",
      mimeType: "application/pdf",
      data,
      metadata: { filename: file.name },
    };
  } else {
    // 其他文件类型：直接使用二进制数据
    const data = await fileToBase64(file);
    return {
      type: "file",
      mimeType: file.type,
      data: data, // 注意：这里需要根据实际 ContentBlock 类型调整
      metadata: {
        filename: file.name,
        size: file.size,
        lastModified: file.lastModified
      },
    };
  }
}

// Helper to convert File to base64 string (用于图片和PDF)
export async function fileToBase64(file: File): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const result = reader.result as string;
      // Remove the data:...;base64, prefix
      resolve(result.split(",")[1]);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

// Helper to convert File to ArrayBuffer (用于其他文件类型)
export async function fileToArrayBuffer(file: File): Promise<ArrayBuffer> {
  return new Promise<ArrayBuffer>((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      resolve(reader.result as ArrayBuffer);
    };
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

// Type guard for Base64ContentBlock
export function isBase64ContentBlock(
  block: unknown,
): block is ContentBlock.Multimodal.Data {
  if (typeof block !== "object" || block === null || !("type" in block))
    return false;

  const blockType = (block as { type: unknown }).type;
  const mimeType = (block as { mimeType?: unknown }).mimeType;

  // file 类型 (支持所有文件类型)
  if (blockType === "file" && typeof mimeType === "string") {
    return true;
  }

  // image 类型
  if (
    blockType === "image" &&
    typeof mimeType === "string" &&
    (mimeType as string).startsWith("image/")
  ) {
    return true;
  }

  return false;
}
