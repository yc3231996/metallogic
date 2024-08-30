import type { IOnCompleted, IOnData, IOnError, IOnFile, IOnMessageEnd, IOnMessageReplace, IOnNodeFinished, IOnNodeStarted, IOnThought, IOnWorkflowFinished, IOnWorkflowStarted } from './base'
import { get, post, ssePost } from './base'
import type { Feedbacktype } from '@/types/app'

export const sendChatMessage = async (
  body: Record<string, any>,
  {
    onData,
    onCompleted,
    onThought,
    onFile,
    onError,
    getAbortController,
    onMessageEnd,
    onMessageReplace,
    onWorkflowStarted,
    onNodeStarted,
    onNodeFinished,
    onWorkflowFinished,
  }: {
    onData: IOnData
    onCompleted: IOnCompleted
    onFile: IOnFile
    onThought: IOnThought
    onMessageEnd: IOnMessageEnd
    onMessageReplace: IOnMessageReplace
    onError: IOnError
    getAbortController?: (abortController: AbortController) => void
    onWorkflowStarted: IOnWorkflowStarted
    onNodeStarted: IOnNodeStarted
    onNodeFinished: IOnNodeFinished
    onWorkflowFinished: IOnWorkflowFinished
  },
) => {
  return ssePost('chat-messages', {
    body: {
      ...body,
      response_mode: 'streaming',
    },
  }, { onData, onCompleted, onThought, onFile, onError, getAbortController, onMessageEnd, onMessageReplace, onNodeStarted, onWorkflowStarted, onWorkflowFinished, onNodeFinished })
}

export const fetchConversations = async () => {
  return get('conversations', { params: { limit: 100, first_id: '' } })
}

export const fetchChatList = async (conversationId: string) => {
  return get('messages', { params: { conversation_id: conversationId, limit: 20, last_id: '' } })
}

// init value. wait for server update
export const fetchAppParams = async () => {
  return get('parameters')
}

export const updateFeedback = async ({ url, body }: { url: string; body: Feedbacktype }) => {
  return post(url, { body })
}

export const generationConversationName = async (id: string) => {
  return post(`conversations/${id}/name`, { body: { auto_generate: true } })
}

export const fetchWorkspaceInfo = async (workspace: string) => {
  //return get(`${workspace}/info`)

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const info = mockWorkspaceInfo[workspace as keyof typeof mockWorkspaceInfo];
      if (info) {
        resolve(info);
      } else {
        resolve('');
        // reject(new Error('Workspace not found'));
      }
    }, 500);
  });
}

const mockWorkspaceInfo = {
  retail: {
    supported_dim: ["时间", "地区", "产品类别", "省份", "渠道"],
    supported_measurement: ["销售额", "订单数", "门店数", "利润"],
    suggested_questions: [
      "计算每个店铺的坪效（每平方米销售额），并按降序排列",
      "展示过去一年的月销售趋势以及环比情况？",
      "分析不同销售渠道的销售占比",
      "找出销售额增长最快的top5产品类别以及销售额占比"
    ]
  },
  mes: {
    supported_dim: ["时间"],
    supported_measurement: ["不良品率", "生产订单数"],
    suggested_questions: [
      "过去30天内不良品率情况，显示主要缺陷类型及数量占比",
      "设备的使用情况",
      "分析最近一周质量检查未通过的产品，找出最常见的失败原因和相关生产批次",
      "显示当前所有进行中生产订单的完成百分比和预计完成时间"
    ]
  }
};
