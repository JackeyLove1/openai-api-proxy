import OpenAI from 'openai'
import { IChat } from './base'
import { openaiBase } from './openai'

export function xai(env: Record<string, string>): IChat {
    const map = {
        "grok-3-mini-beta": "grok-3-mini-beta",
        "grok-3-beta": "grok-3-beta",
    }

    const r = openaiBase({
        createClient: () =>
            new OpenAI({
                apiKey: env.XAI_API_KEY,
                baseURL: 'https://api.xai.com/v1',
            }),
        pre(req) {
            req.model = map[req.model as keyof typeof map]
            return req
        },
    })

    r.name = 'xai'
    r.requiredEnv = ['XAI_API_KEY']
    r.supportModels = Object.keys(map)
    return r
} 