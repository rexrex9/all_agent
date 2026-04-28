from deepagents.middleware import SkillsMiddleware
from deepagents.middleware.skills import _alist_skills,SkillMetadata,SkillsStateUpdate
import asyncio


class MySkillsMiddleware(SkillsMiddleware):

    def _get_backend(self, state, runtime, config):
        return self._backend(runtime)._ensure_backend() # 获取后端实例
    # 方案1
    # async def abefore_agent(self,state,runtime,config):
    #     # 通过重写abefore_agent,然后调用父类的同步before_agent方法，
    #     # 用to_thread将父类方法转为异步方法，以此化解其中包含的线程阻塞操作
    #     await asyncio.to_thread(super().before_agent,state,runtime,config)

    # 方案2
    async def abefore_agent(self, state, runtime, config):
        """Load skills metadata before agent execution (async).

        Loads skills once per session from all configured sources. If
        `skills_metadata` is already present in state (from a prior turn or
        checkpointed session), the load is skipped and `None` is returned.

        Skills are loaded in source order with later sources overriding
        earlier ones if they contain skills with the same name (last one wins).

        Args:
            state: Current agent state.
            runtime: Runtime context.
            config: Runnable config.

        Returns:
            State update with `skills_metadata` populated, or `None` if already present.
        """
        # Skip if skills_metadata is already present in state (even if empty)
        if "skills_metadata" in state:
            return None

        # Resolve backend (supports both direct instances and factory functions)

        # 化解线程阻塞的手段
        backend = await asyncio.to_thread(self._get_backend,state, runtime, config)

        all_skills: dict[str, SkillMetadata] = {}

        # Load skills from each source in order
        # Later sources override earlier ones (last one wins)
        for source_path in self.sources:
            source_skills = await _alist_skills(backend, source_path)
            for skill in source_skills:
                all_skills[skill["name"]] = skill

        skills = list(all_skills.values())
        return SkillsStateUpdate(skills_metadata=skills)








