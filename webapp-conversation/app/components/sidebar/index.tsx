import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import {
  ChatBubbleOvalLeftEllipsisIcon,
  PencilSquareIcon,
  EllipsisHorizontalIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/react/24/outline'
import { ChatBubbleOvalLeftEllipsisIcon as ChatBubbleOvalLeftEllipsisSolidIcon } from '@heroicons/react/24/solid'
import Button from '@/app/components/base/button'
import type { ConversationItem } from '@/types/app'

function classNames(...classes: any[]) {
  return classes.filter(Boolean).join(' ')
}

const MAX_CONVERSATION_LENTH = 40

export type ISidebarProps = {
  copyRight: string
  currentId: string
  onCurrentIdChange: (id: string) => void
  list: ConversationItem[]
  onRename: (id: string) => void
  onDelete: (id: string) => void
}

const Sidebar: FC<ISidebarProps> = ({
  copyRight,
  currentId,
  onCurrentIdChange,
  list,
  onRename,
  onDelete,
}) => {
  const { t } = useTranslation()
  const [activeMenu, setActiveMenu] = useState<string | null>(null)

  const renderDropdownMenu = (itemId: string) => (
    <div className="relative inline-block text-left">
      <button
        className="p-1 rounded-full hover:bg-gray-200 transition-opacity duration-200 opacity-0 group-hover:opacity-100"
        onClick={(e) => {
          e.stopPropagation()
          setActiveMenu(activeMenu === itemId ? null : itemId)
        }}
      >
        <EllipsisHorizontalIcon className="h-5 w-5 text-gray-500" aria-hidden="true" />
      </button>

      {activeMenu === itemId && (
        <div 
          className="absolute right-full top-0 mr-1 w-36 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-20"
          onMouseLeave={() => setActiveMenu(null)}
        >
          <div className="py-1">
            <button
              onClick={(e) => {
                e.stopPropagation()
                onRename(itemId)
                setActiveMenu(null)
              }}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
            >
              <PencilIcon className="mr-3 h-4 w-4" aria-hidden="true" />
              Rename
            </button>
            <button
              onClick={(e) => {
                e.stopPropagation()
                onDelete(itemId)
                setActiveMenu(null)
              }}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
            >
              <TrashIcon className="mr-3 h-4 w-4" aria-hidden="true" />
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  )

  return (
    <div className="shrink-0 flex flex-col overflow-y-auto bg-white pc:w-[244px] tablet:w-[192px] mobile:w-[240px] border-r border-gray-200 tablet:h-[calc(100vh_-_3rem)] mobile:h-screen">
      {list.length < MAX_CONVERSATION_LENTH && (
        <div className="flex flex-shrink-0 p-4 !pb-0">
          <Button
            onClick={() => { onCurrentIdChange('-1') }}
            className="group block w-full flex-shrink-0 !justify-start !h-9 text-primary-600 items-center text-sm">
            <PencilSquareIcon className="mr-2 h-4 w-4" /> {t('app.chat.newChat')}
          </Button>
        </div>
      )}

      <nav className="mt-4 flex-1 space-y-1 bg-white p-4 !pt-0">
        {list.map((item) => {
          const isCurrent = item.id === currentId
          const ItemIcon
            = isCurrent ? ChatBubbleOvalLeftEllipsisSolidIcon : ChatBubbleOvalLeftEllipsisIcon
          return (
            <div
              key={item.id}
              className={classNames(
                isCurrent
                  ? 'bg-primary-50 text-primary-600'
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-700',
                'group flex items-start justify-between rounded-md px-2 py-2 text-sm font-medium cursor-pointer relative'
              )}
            >
              <div 
                className="flex items-start flex-grow"
                onClick={() => onCurrentIdChange(item.id)}
              >
                <ItemIcon
                  className={classNames(
                    isCurrent
                      ? 'text-primary-600'
                      : 'text-gray-400 group-hover:text-gray-500',
                    'mr-3 h-5 w-5 flex-shrink-0 mt-0.5'
                  )}
                  aria-hidden="true"
                />
                <span className="break-words">{item.name}</span>
              </div>
              {renderDropdownMenu(item.id)}
            </div>
          )
        })}
      </nav>
      <div className="flex flex-shrink-0 pr-4 pb-4 pl-4">
        <div className="text-gray-400 font-normal text-xs">© {copyRight} {(new Date()).getFullYear()}</div>
      </div>
    </div>
  )
}

export default React.memo(Sidebar)