import { Router } from 'express';
import health from './health.route';
import sample from './sample.route';

const router = Router();

router.use('/health', health);
router.use('/sample', sample);

export default router;