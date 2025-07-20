import React from 'react'
import "./Search.css"
import searchIcon from "../../../../assets/Icons/searchIcon.svg"
import { memo } from 'react'

function Search({userId}) {
  return (
    <div className="search-input">
        <input type="text" id='search-input' placeholder='search...' />
        <button><img src={searchIcon} id='search-sumbit-btn' alt="search-icon" /></button>
    </div>
  )
}

export default memo(Search)