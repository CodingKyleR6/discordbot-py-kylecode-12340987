import requests
from ics import Calendar
import discord
from datetime import datetime, timedelta

# Discord 봇 구현
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/EPL'):
        try:
            # ICS 파일 다운로드 및 파싱하여 이벤트 정보 추출
            url = 'https://calendar.google.com/calendar/ical/98vpe1b8ud40q2jdmacdmdbii0%40group.calendar.google.com/private-ed79b1214ec06437baa09d3889d48181/basic.ics'
            response = requests.get(url)
            c = Calendar(response.text)
            events = []
            for event in c.events:
                start_time = event.begin.datetime
                end_time = event.end.datetime
                start_time_kst = start_time + timedelta(hours=9)  # UTC to KST (+9)
                end_time_kst = end_time + timedelta(hours=9)  # UTC to KST (+9)
                events.append({
                    'start': start_time_kst.strftime('%Y/%m/%d %H:%M'),
                    'end': end_time_kst.strftime('%Y/%m/%d %H:%M'),
                    'name': event.name,
                    'location': event.location,
                    'description': event.description
                })

            # 이벤트를 날짜별로 그룹화
            events_by_date = {}
            for event in events:
                # 이벤트의 시작 날짜 가져오기
                start_date = datetime.strptime(event['start'], '%Y/%m/%d %H:%M').date()
                # 딕셔너리에 해당 날짜가 없으면 추가
                if start_date not in events_by_date:
                    events_by_date[start_date] = []
                events_by_date[start_date].append(event)

            # 날짜별 이벤트 정보를 텍스트로 변환하여 채팅창에 출력
            response = 'EPL Schedule:\n\n'
            for date, events_on_date in events_by_date.items():
                response += f'{date.strftime("%Y/%m/%d")}:\n'
                for event in events_on_date:
                    response += f'{event["start"]} - {event["end"]}: {event["name"]} ({event["location"]})\n'
                response += '\n'

            # 메시지 분할
            remaining_message = ''
            if len(response) > 0:
                response = remaining_message + response
                await message.channel.send(response[:2000])
                remaining_message = response[2000:]
                while len(remaining_message) > 0 and len(remaining_message) > 1999:
                    await message.channel.send(remaining_message[:1999])
                    remaining_message = remaining_message[1999:]
                if len(remaining_message) > 0:
                    await message.channel.send(remaining_message)

        except Exception as e:
            await message.channel.send(f'Error occurred: {e}')


# Discord 봇 실행
client.run('TOKEN')
