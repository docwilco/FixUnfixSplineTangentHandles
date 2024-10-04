# FixUnfixSplineTangentHandles

## Purpose

In Fusion 360, if you scale splines in a sketch, the tangent handles will scale
with the spline, which causes the spline to change shape. This script will fix
the tangent handles so that they don't scale with the spline. It will also unfix
them if they are all fixed, so that you can then edit them again after scaling.

## Installation

Clone this repo into your Scripts folder. For windows this is
`%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts`. On OSX this is:
`"$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/"`

## Usage

You can run it from Utilities > Scripts and Add-Ins. It will be called
`FixUnfixSplineTangentHandles`.

If you have both fixed and unfixed or only unfixed tangent handles, it will fix
the unfixed ones. If you have only fixed handles it will unfix all of them.

It will tell you what it's about to do, giving you a chance to cancel if you
change your mind.

Changelog

- 0.1.1: Add privacy policy
- 0.1.0: Initial release