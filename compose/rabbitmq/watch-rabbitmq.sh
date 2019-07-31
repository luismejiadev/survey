#!/bin/bash
watch -d '/usr/sbin/rabbitmqctl list_queues -p survey_app name messages messages_ready messages_unacknowledged consumers| sort'