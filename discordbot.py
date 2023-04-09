{
  "import": [
    {
      "name": "requests"
    },
    {
      "name": "ics",
      "children": [
        {
          "name": "Calendar"
        }
      ]
    },
    {
      "name": "discord",
      "children": [
        {
          "name": "Client",
          "attributes": {
            "intents": ["GUILDS", "GUILD_MESSAGES"]
          }
        },
        {
          "name": "Intents",
          "attributes": {
            "GUILDS": true,
            "GUILD_MESSAGES": true
          }
        }
      ]
    },
    {
      "name": "datetime",
      "children": [
        {
          "name": "datetime"
        },
        {
          "name": "timedelta"
        }
      ]
    }
  ],
  "client": {
    "on_ready": {
      "name": "async",
      "parameters": [
        "client"
      ],
      "body": [
        {
          "name": "print",
          "parameters": [
            {
              "value": "{client.user} has connected to Discord!"
            }
          ]
        }
      ]
    },
    "on_message": {
      "name": "async",
      "parameters": [
        "message"
      ],
      "body": [
        {
          "name": "if",
          "parameters": [
            {
              "name": "message.author",
              "property": "bot"
            },
            {
              "name": "return"
            }
          ]
        },
        {
          "name": "if",
          "parameters": [
            {
              "name": "message.content",
              "property": "startswith",
              "args": [
                "/EPL"
              ]
            },
            {
              "try": {
                "body": [
                  {
                    "name": "set",
                    "parameters": [
                      {
                        "name": "url",
                        "value": "https://calendar.google.com/calendar/ical/98vpe1b8ud40q2jdmacdmdbii0%40group.calendar.google.com/private-ed79b1214ec06437baa09d3889d48181/basic.ics"
                      }
                    ]
                  },
                  {
                    "name": "set",
                    "parameters": [
                      {
                        "name": "response",
                        "value": {
                          "name": "requests.get",
                          "parameters": [
                            {
                              "name": "url"
                            }
                          ]
                        }
                      }
                    ]
                  },
                  {
                    "name": "set",
                    "parameters": [
                      {
                        "name": "c",
                        "value": {
                          "name": "Calendar",
                          "parameters": [
                            {
                              "name": "response.text"
                            }
                          ]
                        }
                      }
                    ]
                  },
                  {
                    "name": "set",
                    "parameters": [
                      {
                        "name": "events",
                        "value": []
                      }
                    ]
                  },
                  {
                    "name": "for",
                    "parameters": [
                      {
                        "name": "event",
                        "value": {
                          "name": "c.events"
                        }
                      }
                    ],
                    "body": [
                      {
                        "name": "set",
                        "parameters": [
                          {
                            "name": "start_time",
                            "property": "event.begin.datetime"
                          }
                        ]
                      },
                      {
                        "name": "set",
                        "parameters": [
                          {
                            "name": "end_time",
                            "property": "
