import React from 'react'

export default function Title({title, fontSize, margin}) {
  return (
    <h1 style={{fontSize, margin, color: ' #77C0F6'}}>
        {title}
    </h1>
  )
}
