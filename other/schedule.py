# -*- coding: utf-8 -*-

# Use this file to easily define all of your cron jobs.
#
# It's helpful to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron
#
# Learn more: http://github.com/fengsp/plan

from plan import Plan

cron = Plan()

# register one command, script or module
# cron.command('command', every='1.day')
# cron.script('script.py', path='/web/yourproject/scripts', every='1.month')
# cron.module('calendar', every='feburary', at='day.3')

if __name__ == "__main__":
    cron.run()
