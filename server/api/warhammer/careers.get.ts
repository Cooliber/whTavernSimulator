/**
 * API endpoint for Warhammer careers data
 */
import { readFileSync } from 'fs'
import { join } from 'path'

export default defineEventHandler(async (event) => {
  try {
    // Path to the careers JSON file
    const filePath = join(process.cwd(), 'plugins/warhammer-pl/compendium/wfrp4e-core.careers.json')
    
    // Read and parse the JSON file
    const fileContent = readFileSync(filePath, 'utf-8')
    const data = JSON.parse(fileContent)
    
    // Return the data with proper headers
    setHeader(event, 'Content-Type', 'application/json')
    setHeader(event, 'Cache-Control', 'public, max-age=3600') // Cache for 1 hour
    
    return {
      success: true,
      data: data,
      timestamp: new Date().toISOString()
    }
  } catch (error) {
    console.error('Error loading careers data:', error)
    
    setResponseStatus(event, 500)
    return {
      success: false,
      error: 'Failed to load careers data',
      message: error instanceof Error ? error.message : 'Unknown error'
    }
  }
})
