import asyncio
from ..models.channel_message_model import ChannelMessage
from ..storage_manager.channel_message_data_manager_interface import ChannelMessageDataManagerInterface
from ..instances.create_async_engine import AsyncSessionLocal
from ..instances.elastic_search_engine import es_elastic_search_engine as es
from ..configuartions.channel_message_index_mapper import mapping_channel_message_index
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import datetime

class ChannelMessageDataManager(ChannelMessageDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal
        
    async def create_message(self, channel_id, sender_id, content):
        timestamp = datetime.datetime.utcnow()
              
        async with self.db_session_factory() as session:
            try: 
                new_message = ChannelMessage(
                    channel_id=channel_id,
                    sender_id=sender_id,
                    content=content,
                    timestamp=timestamp,
                )
                session.add(new_message)
                await session.commit()
                await session.refresh(new_message)
                await mapping_channel_message_index([new_message])
                return new_message          
            except Exception as e:
                print(f"Error creating message: {e}")
                await session.rollback()
                return None
            
    async def get_channel_messages_by_id(self, channel_id, search_index=[]):
        print(f"State of search index : {search_index}")
        async with self.db_session_factory() as session:
            try:
                channel_message_id_query = await session.execute(select(ChannelMessage).filter_by(channel_id=channel_id))
                messages = channel_message_id_query.scalars().all()
                if not search_index: 
                    if messages:  
                        await mapping_channel_message_index(messages)
                return messages
            except Exception as e:
                print(f"Error fetching channel message: {e}")
                return None
            
    async def get_all_messages(self):       
        async with self.db_session_factory() as session:
            try:
                all_messages = await session.execute(select(ChannelMessage))
                return all_messages.scalars().all()
            except Exception as e:
                print(f"Error fetching all messages: {e}")
                return None