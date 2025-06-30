import { Request, Response, Router } from 'express';

const router = Router();

router.get('/health', async (req: Request, res: Response) => {
  try {
    res.status(200).json({
      message: 'Service is healthy',
      status: 200
    });
  } catch (error) {
    console.error('An error ocurred:', error);
    res.status(500).json(error);
  }
});

export default router;